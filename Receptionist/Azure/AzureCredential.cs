using Azure.Core;
using Azure.Identity;

namespace Receptionist.Bot.Azure
{
    /// <summary>
    /// Utility class that exposes Azure credentials for making authenticated API calls.
    /// </summary>
    public class AzureCredential
    {
        public static TokenCredential? TokenCredential { get; set; }
        
        /// <summary>
        /// Sets the TokenCredential property. Initialize() must be called before TokenCredential is used.
        /// </summary>
        /// <returns></returns>
        public static void Initialize() => TokenCredential = new DefaultAzureCredential();
    }
}
