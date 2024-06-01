using System.Text.Json.Serialization;

namespace Receptionist.Bot.Models
{
    public class FoundationaLLMResponseModel
    {
        /// <summary>
        /// The completion text.
        /// </summary>
        [JsonPropertyName("text")]
        public string? Text { get; set; }
    }
}
