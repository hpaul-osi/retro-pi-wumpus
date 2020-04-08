using OSIsoft.Data;
using OSIsoft.Data.Http;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace VotePolling
{    
    public class SDSWumpusData
    {
        private string _wumpusType = "WumpusActionVoteV2";
        private string _gameStream = "WumpusGameStream";
        private string _wumpusDescription = "Wumpus Action Vote stream with action enum.";

        private string tenantId = "906a9f59-2c0b-4ebf-b554-83be70f62758"; // configuration["TenantId"];
        private string namespaceId = "Wumpus"; // configuration["NamespaceId"];
        private string resource = "https://staging.osipi.com"; // configuration["Resource"];
        private string clientId = "dd9554ad-bf02-427b-aa0d-c01d5d81f030"; // configuration["ClientId"];
        private string clientKey = "gWhHg7w3nExNFlk/mvYpsBwMSKi9p0/b+vMeylGGaXE="; // configuration["ClientKey"];

        private AuthenticationHandler authenticationHandler;
        private SdsService sdsService;
        private ISdsMetadataService metadataService;
        private ISdsDataService dataService;

        public SDSWumpusData()
        {
            var uriResource = new Uri(resource);
            // Step 1 
            // Get Sds Services to communicate with server
            authenticationHandler = new AuthenticationHandler(uriResource, clientId, clientKey);
            sdsService =
                new SdsService(new Uri(resource), null, HttpCompressionMethod.GZip, authenticationHandler);
            metadataService = sdsService.GetMetadataService(tenantId, namespaceId);
            dataService = sdsService.GetDataService(tenantId, namespaceId);
            // var tableService = sdsService.GetTableService(tenantId, namespaceId);
            Console.WriteLine($"SDS endpoint at {resource}");
            Console.WriteLine();


        }
        public async Task<SdsType> GetWumpusType()
        {
            
            /*SdsType simpleType = SdsTypeBuilder.CreateSdsType<WumpusActionVote>();
            simpleType.Id = "WumpusActionVoteV3";
            simpleType.Name = "WumpusActionVoteV3";
            simpleType.Description = "Wumpus Action Vote stream with action enum.";
            var type = await metadataService.GetOrCreateTypeAsync(simpleType);*/

            var type = await metadataService.GetTypeAsync(_wumpusType);

            return type;
        }

        public async Task<SdsStream> GetWumpusStream()
        {
            var stream = new SdsStream
            {
                Id = _gameStream,
                Name = "Wave Data Sample",
                TypeId = _wumpusType,
                Description = "This is a sample SdsStream for storing WaveData type measurements"
            };
            stream = await metadataService.GetOrCreateStreamAsync(stream);

            return stream;
        }

        public async Task InsertWumpusValue(WumpusActionVote wumpusActionVote)
        {            
            await dataService.InsertValueAsync(_gameStream, wumpusActionVote);            
        }

    }    
}
