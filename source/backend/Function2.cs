using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using VotePolling.DataModel;
using System.Collections.Generic;
using System.Linq;

namespace VotePolling
{
    public static class Function2
    {
        [FunctionName("AggregateVotes")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");

            int moveNumber = int.Parse(req.Query["MoveNumber"]);

            var sDSWumpusData = new SDSWumpusData();            

            string maxRepeatedItem;
            try
            {
                var wumpusActionVotes = await sDSWumpusData.AggregateWumpusDataValue(moveNumber);
                maxRepeatedItem = wumpusActionVotes.GroupBy(x => x.WumpusAction)
                          .OrderByDescending(x => x.Count())
                          .First().Key;
            }
            catch (Exception ex)
            {
                log.LogError("There was an error in getting aggregrate value", ex);
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
            
            return new OkObjectResult(new Result { voteResult = maxRepeatedItem });
        }
    }
}
