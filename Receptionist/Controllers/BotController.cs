using Microsoft.AspNetCore.Mvc;
using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Microsoft.Bot.Builder;

namespace Receptionist.Bot.Controllers
{
    [Route("api/messages")]
    [ApiController]
    public class BotController(IBotFrameworkHttpAdapter adapter, IBot bot) : ControllerBase
    {
        private readonly IBotFrameworkHttpAdapter _adapter = adapter;
        private readonly IBot _bot = bot;

        [HttpPost, HttpGet]
        public async Task PostAsync()
        {
            // Delegate the processing of the HTTP POST to the adapter.
            // The adapter will invoke the bot.
            await _adapter.ProcessAsync(Request, Response, _bot);
        }
    }
}
