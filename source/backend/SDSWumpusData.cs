using OSIsoft.Data;
using OSIsoft.Data.Http;
using OSIsoft.Data.Reflection;
using OSIsoft.Identity;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using VotePolling.DataModel;

namespace VotePolling
{    
    public class SDSWumpusData
    {
        private string _wumpusType = "WumpusActionVoteV8";
        private string _gameStream = "WumpusGameStreamV8";
        private string _wumpusDescription = "Wumpus Action Vote stream with action enum.";

        private string tenantId = "906a9f59-2c0b-4ebf-b554-83be70f62758"; // configuration["TenantId"];
        private string namespaceId = "Wumpus"; // configuration["NamespaceId"];
        private string resource = "https://staging.osipi.com"; // configuration["Resource"];
        private string clientId = "4e7605fb-4ba3-4151-9fa1-9dc12adc0bf7"; // configuration["ClientId"];
        private string clientKey = ""; // configuration["ClientKey"];

        private AuthenticationHandler authenticationHandler;
        private SdsService sdsService;
        private ISdsMetadataService metadataService;
        private ISdsDataService dataService;        

        public SDSWumpusData()
        {
            var uriResource = new Uri(resource);

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
        public async Task<SdsType> GetOrCreateWumpusType()
        {
            
            SdsType simpleType = SdsTypeBuilder.CreateSdsType<WumpusActionVote>();
            simpleType.Id = _wumpusType;
            simpleType.Name = _wumpusType;
            simpleType.Description = "Wumpus Action Vote stream with action enum.";
            /*var retType = await metadataService.GetTypeAsync(simpleType.Id);

            if (retType != null)
            {
                return retType;
            }*/

            var type = await metadataService.GetOrCreateTypeAsync(simpleType);

            return type;
        }

        public async Task<SdsStream> GetOrCreateWumpusStream()
        {
            var stream = new SdsStream
            {
                Id = _gameStream,
                Name = "Wave Data Sample",
                TypeId = _wumpusType,
                Description = "This is a sample SdsStream for storing WaveData type measurements"
            };
            /*var retStream = await metadataService.GetStreamAsync(stream.Id);

            if (retStream != null)
            {
                return retStream;
            }*/
            stream = await metadataService.GetOrCreateStreamAsync(stream);

            return stream;
        }

        public async Task InsertWumpusValue(WumpusActionVote wumpusActionVote)
        {            
            await dataService.InsertValueAsync(_gameStream, wumpusActionVote);            
        }

        public async Task<IEnumerable<WumpusActionVote>> AggregateWumpusDataValue(int moveNumber)
        {
            // await dataService.GetValueAsync<VoteAggregationQuery>();
            return (await dataService.GetFilteredValuesAsync<WumpusActionVote>(_gameStream, 
                $"moveNumber eq {moveNumber}")).ToList();
        }
    }    
}
