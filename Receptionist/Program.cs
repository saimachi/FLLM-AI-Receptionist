using Microsoft.Bot.Builder;
using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Receptionist.Bot.Azure;
using Receptionist.Bot.Bots;
using Receptionist.Bot.Middleware;
using Receptionist.Bot.Services;

var builder = WebApplication.CreateBuilder(args);

AzureCredential.Initialize();

builder.Services.AddTransient<BearerTokenHandler>();
builder.Services.AddHttpClient<FoundationaLLMService>(client =>
{
    client.BaseAddress = new Uri(
        builder.Configuration.GetRequiredSection(Receptionist.Bot.Configuration.Constants.FOUNDATIONALLM_COREAPI_CONFIG_SECTION)
                             .GetValue<string>(Receptionist.Bot.Configuration.Constants.URL_CONFIG_KEY)!
    );
})
.AddHttpMessageHandler<BearerTokenHandler>();

builder.Services.AddSingleton<IBotFrameworkHttpAdapter, CloudAdapter>();
builder.Services.AddTransient<IBot, ReceptionistBot>();
builder.Services.AddControllers();

var app = builder.Build();

app.UseWebSockets();
app.MapDefaultControllerRoute();

app.Run();
