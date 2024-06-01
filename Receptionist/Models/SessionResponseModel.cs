namespace Receptionist.Bot.Models
{
    public class SessionResponseModel
    {
        /// <summary>
        /// The unique identifier.
        /// </summary>
        public string Id { get; set; }
        /// <summary>
        /// The type of the session.
        /// </summary>
        public string Type { get; set; }

        /// <summary>
        /// The Partition key.
        /// </summary>
        public string SessionId { get; set; }
        /// <summary>
        /// The number of tokens used in the session.
        /// </summary>
        public int? TokensUsed { get; set; }
        /// <summary>
        /// The name of the session.
        /// </summary>
        public string Name { get; set; }
        /// <summary>
        /// The UPN of the user who created the chat session.
        /// </summary>
        public string UPN { get; set; }
        /// <summary>
        /// Deleted flag used for soft delete.
        /// </summary>
        public bool Deleted { get; set; }
    }
}
