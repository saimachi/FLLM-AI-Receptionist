﻿using Azure.Core;
using Receptionist.Bot.Azure;
using Receptionist.Bot.Configuration;

namespace Receptionist.Bot.Middleware
{
    /// <summary>
    /// Appends an authentication token to all outbound requests to the FoundationaLLM Core API.
    /// </summary>
    /// <param name="configuration">Injected instance of IConfiguration.</param>
    public class BearerTokenHandler(IConfiguration configuration) : DelegatingHandler
    {
        /// <summary>
        /// Obtains an authentication token using the scope in appsettings.json and adds it to the HttpClient request pipeline.
        /// </summary>
        /// <param name="request"></param>
        /// <param name="cancellationToken"></param>
        /// <returns></returns>
        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            var scope = configuration.GetRequiredSection(Constants.FOUNDATIONALLM_COREAPI_CONFIG_SECTION)
                                      .GetValue<string>(Constants.SCOPE_CONFIG_KEY);
            scope = scope![..scope!.LastIndexOf('/')] + "/.default";

            var accessToken = AzureCredential.TokenCredential!.GetToken(
                new TokenRequestContext([scope!]),
                default
            );

            request.Headers.Add("Authorization", $"Bearer {accessToken.Token}");

            return await base.SendAsync(request, cancellationToken);
        }
    }
}
