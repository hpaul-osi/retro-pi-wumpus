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
        [FunctionName("VotePolling")]
        public static async Task<IActionResult> Run(
            [HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");

            string name = req.Query["name"];

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            var data = JsonConvert.DeserializeObject<WumpusActionVote>(requestBody);
            // name = name ?? data?.name;

            var sDSWumpusData = new SDSWumpusData();
            var voteData = (WumpusActionVote)data;
            await sDSWumpusData.InsertWumpusValue(voteData);

            string responseMessage = string.IsNullOrEmpty(name)
                ? "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."
                : $"Hello, {name}. This HTTP triggered function executed successfully.";

            return new OkObjectResult(true);
        }
    }
}
