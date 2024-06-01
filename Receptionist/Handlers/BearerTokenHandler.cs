using Azure.Core;
using Receptionist.Bot.Azure;
using Receptionist.Bot.Configuration;

namespace Receptionist.Bot.Middleware
{
    public class BearerTokenHandler(IConfiguration configuration) : DelegatingHandler
    {
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
