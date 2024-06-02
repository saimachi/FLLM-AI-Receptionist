using Receptionist.Bot.Models;

namespace Receptionist.Bot.Interfaces
{
    /// <summary>
    /// Utilities to interface with the FoundationaLLM Core API.
    /// </summary>
    public interface IFoundationaLLMService
    {
        /// <summary>
        /// Creates a new FoundationaLLM Chat Session.
        /// </summary>
        /// <returns>The properties of the new session.</returns>
        Task<SessionResponseModel> CreateSession();
        /// <summary>
        /// Send a completion request to FoundationaLLM. The session in the request must already be created.
        /// </summary>
        /// <param name="request">Completion request to send.</param>
        /// <returns>Response from the agent.</returns>
        Task<FoundationaLLMResponseModel> GetFoundationaLLMResponse(FoundationaLLMRequestModel request);
    }
}
