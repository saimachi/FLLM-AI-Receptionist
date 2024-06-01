using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Receptionist.Bot.Services;

namespace Receptionist.Bot.Bots
{
    public class ReceptionistBot : ActivityHandler
    {
        private readonly FoundationaLLMService _foundationaLLMService;

        public ReceptionistBot(FoundationaLLMService foundationaLLMService)
        {
            _foundationaLLMService = foundationaLLMService;
        }

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            // TODO: Check text for hateful content
            var replyText = "Sure! Let me see what I can do.";
            await turnContext.SendActivityAsync(MessageFactory.Text(replyText, replyText), cancellationToken);
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            var welcomeText = "Hello and welcome!";
            foreach (var member in membersAdded)
            {
                await _foundationaLLMService.CreateSession();
                if (member.Id != turnContext.Activity.Recipient.Id)
                {
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText, welcomeText), cancellationToken);
                }
            }
        }
    }
}
