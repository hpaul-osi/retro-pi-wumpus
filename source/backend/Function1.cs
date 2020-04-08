using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System.Collections.Generic;
using System.Timers;

namespace FunctionApp1
{
    public static class Function1
    {
        static List<string> users = new List<string>();
        static Timer timer = new Timer();
        static Object lockOfList = new Object();
        static Object lockOfTimer = new Object();
        static double votingInterval = 5000; // Voting resets every 5 seconds
        static int VoteRoundNumber = 0;
        
        [FunctionName("RegisterUser")]
        public static async Task<IActionResult> RegisterUser(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");

            string name = req.Query["name"];

            string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
            dynamic data = JsonConvert.DeserializeObject(requestBody);
            name = name ?? data?.name;

            if (name != null)
            {
                lock (lockOfList)
                {
                    users.Add(name);
                }
                return (ActionResult)new OkResult();
            }
            else
            {
                return new BadRequestObjectResult("Please pass a name on the query string or in the request body");
            }
        }

        [FunctionName("ListUsers")]
        public static async Task<IActionResult> ListUsers(
           [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
           ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a ListUsers request.");
            return (ActionResult)new OkObjectResult(users);
        }

        [FunctionName("StartGame")]
        public static async Task<IActionResult> StartGame(
            [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = null)] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a StartGame request.");

            if (!timer.Enabled)
            {
                lock (lockOfTimer)
                {
                    if (!timer.Enabled)
                    {
                        timer.Enabled = true;
                        timer.AutoReset = true;
                        timer.Interval = votingInterval;
                        timer.Elapsed += OnTimerElapsed;
                        timer.Start();
                    }
                }
            }

            return (ActionResult)new OkResult();
        }


        [FunctionName("TryGetResult")]
        public static async Task<IActionResult> TryGetResult(
           [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req,
           ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a TryGetResult request.");

            string roundNumber = req.Query["VoteRoundNumber"];

            if (string.IsNullOrEmpty(roundNumber))
                return new BadRequestObjectResult("Please pass a VoteRoundNumber on the query string.");

            if (int.Parse(roundNumber) <= VoteRoundNumber)
            {
                //ToDo: return (ActionResult)new OkObjectResult(AggregratedResult(roundNumber));
                return (ActionResult)new OkResult();
            }
            else
            {
                return (ActionResult)new NoContentResult(); // Use NoContent to indicate not-ready
            }
        }

        static void OnTimerElapsed(Object source, ElapsedEventArgs e) 
        {
            VoteRoundNumber++;
        }
    }
}
