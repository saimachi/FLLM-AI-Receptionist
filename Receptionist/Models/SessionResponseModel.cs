using System.Text.Json.Serialization;

namespace Receptionist.Bot.Models
{
    public class SessionResponseModel
    {
        /// <summary>
        /// The unique identifier.
        /// </summary>
        [JsonPropertyName("id")]
        public string Id { get; set; }
        /// <summary>
        /// The type of the session.
        /// </summary>
        [JsonPropertyName("type")]
        public string Type { get; set; }

        /// <summary>
        /// The Partition key.
        /// </summary>
        [JsonPropertyName("sessionId")]
        public string SessionId { get; set; }
        /// <summary>
        /// The number of tokens used in the session.
        /// </summary>
        [JsonPropertyName("tokensUsed")]
        public int? TokensUsed { get; set; }
        /// <summary>
        /// The name of the session.
        /// </summary>
        [JsonPropertyName("name")]
        public string Name { get; set; }
        /// <summary>
        /// The UPN of the user who created the chat session.
        /// </summary>
        [JsonPropertyName("upn")]
        public string UPN { get; set; }
        /// <summary>
        /// Deleted flag used for soft delete.
        /// </summary>
        [JsonPropertyName("deleted")]
        public bool Deleted { get; set; }
    }
}
