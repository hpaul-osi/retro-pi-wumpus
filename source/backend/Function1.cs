using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using OSIsoft.Identity;
using OSIsoft.Data;
using OSIsoft.Data.Http;

namespace VotePolling
{
    public static class Function1
    {
        [FunctionName("InsertVote")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");            

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            var data = JsonConvert.DeserializeObject<WumpusActionVote>(requestBody);            

            var sDSWumpusData = new SDSWumpusData();            
            await sDSWumpusData.GetOrCreateWumpusType();
            await sDSWumpusData.GetOrCreateWumpusStream();
            try
            {
                await sDSWumpusData.InsertWumpusValue(data);
            }
            catch(Exception ex)
            {
                log.LogError("There was an error in inserting the value", ex);
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
            
            return new OkObjectResult(true);
        }
    }
}
