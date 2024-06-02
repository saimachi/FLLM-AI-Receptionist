using System.Text.Json.Serialization;

namespace Receptionist.Bot.Models
{
    /* 
     * This class is from the FoundationaLLM Source Code: https://github.com/solliancenet/foundationallm
     * It will be removed once the C# SDK is provided.
    */
    public class FoundationaLLMResponseModel
    {
        /// <summary>
        /// The completion text.
        /// </summary>
        [JsonPropertyName("text")]
        public string? Text { get; set; }
    }
}
