using OSIsoft.Data;
using System;
using System.Collections.Generic;
using System.Dynamic;
using System.Text;
using VotePolling.DataModel;

namespace VotePolling
{
    public class WumpusActionVote
    {
        [SdsMember(IsKey = true, Order = 0)]
        public DateTime TimeStamp { get; set; }
        public int MoveNumber { get; set; } // make it int
        public WumpusAction WumpusAction { get; set; }
        public int Room { get; set; }
        public string UserName { get; set; }
    }
}
