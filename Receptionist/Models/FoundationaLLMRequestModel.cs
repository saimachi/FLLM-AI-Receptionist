using System.Text.Json.Serialization;

namespace Receptionist.Bot.Models
{
    public class FoundationaLLMRequestModel
    {
        /// <summary>
        /// The session ID.
        /// </summary>
        [JsonPropertyName("session_id")]
        public string? SessionId { get; set; }

        /// <summary>
        /// Represent the input or user prompt.
        /// </summary>
        [JsonPropertyName("user_prompt")]
        public required string UserPrompt { get; set; }

        /// <summary>
        /// The name of the selected agent.
        /// </summary>
        [JsonPropertyName("agent_name")]
        public string? AgentName { get; set; }
    }
}
