using Azure.Core;
using Azure.Identity;

namespace Receptionist.Bot.Azure
{
    public class AzureCredential
    {
        public static TokenCredential? TokenCredential { get; set; }
        
        public static void Initialize()
        {
            TokenCredential = new DefaultAzureCredential();
        }
    }
}
