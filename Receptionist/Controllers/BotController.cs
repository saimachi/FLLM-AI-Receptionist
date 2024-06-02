using Microsoft.AspNetCore.Mvc;
using Microsoft.Bot.Builder.Integration.AspNet.Core;
using Microsoft.Bot.Builder;

namespace Receptionist.Bot.Controllers
{
    /// <summary>
    /// Handles messages directed to the Receptionist bot.
    /// </summary>
    [Route("api/messages")]
    [ApiController]
    public class BotController(IBotFrameworkHttpAdapter adapter, IBot bot) : ControllerBase
    {
        private readonly IBotFrameworkHttpAdapter _adapter = adapter;
        private readonly IBot _bot = bot;

        /// <summary>
        /// Send the request to the downstream bot implementation.
        /// </summary>
        /// <returns></returns>
        [HttpPost, HttpGet]
        public async Task PostAsync() => await _adapter.ProcessAsync(Request, Response, _bot);
    }
}
