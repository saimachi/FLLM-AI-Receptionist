using Receptionist.Bot.Interfaces;
using Receptionist.Bot.Models;
using System.Text.Json;

namespace Receptionist.Bot.Services
{
    /// <summary>
    /// Utilities to interface with the FoundationaLLM Core API.
    /// </summary>
    public class FoundationaLLMService(HttpClient httpClient) : IFoundationaLLMService
    {
        private readonly HttpClient _httpClient = httpClient;

        /// <inheritdoc/>
        public async Task<SessionResponseModel> CreateSession()
        {
            var newSession = await _httpClient.PostAsync("/sessions", null);
            if (newSession.IsSuccessStatusCode)
            {
                var newSessionData = await newSession.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<SessionResponseModel>(newSessionData!) ?? throw new Exception($"Failed to deserialize session data: {newSessionData}");
            }
            throw new Exception($"Failed to create new session: {newSession.ReasonPhrase}");
        }

        /// <inheritdoc/>
        public async Task<FoundationaLLMResponseModel> GetFoundationaLLMResponse(FoundationaLLMRequestModel request)
        {
            var completionResponse = await _httpClient.PostAsync($"/sessions/{request.SessionId}/completion", JsonContent.Create(request));
            if (completionResponse.IsSuccessStatusCode)
            {
                var completionResponseData = await completionResponse.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<FoundationaLLMResponseModel>(completionResponseData!) ?? throw new Exception($"Failed to deserialize completion response: {completionResponseData}");
            }
            throw new Exception($"Failed to process completion request: {completionResponse.ReasonPhrase}");
        }
    }
}
