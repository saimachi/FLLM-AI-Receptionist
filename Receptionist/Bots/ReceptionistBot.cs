using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Receptionist.Bot.Models;
using Receptionist.Bot.Services;
using System.Collections.Concurrent;

namespace Receptionist.Bot.Bots
{
    public class ReceptionistBot (FoundationaLLMService foundationaLLMService) : ActivityHandler
    {
        private readonly ConcurrentDictionary<string, string> usersAndSessions = new();

        protected override async Task OnMessageActivityAsync(ITurnContext<IMessageActivity> turnContext, CancellationToken cancellationToken)
        {
            // TODO: Check text for hateful content
            var replyText = "Sure! Let me see what I can do.";
            await turnContext.SendActivityAsync(MessageFactory.Text(replyText, replyText), cancellationToken);

            usersAndSessions.TryGetValue(turnContext.Activity.From.Id, out string? sessionId);
            if (sessionId == null)
            {
                var session = await foundationaLLMService.CreateSession();
                usersAndSessions.TryAdd(turnContext.Activity.From.Id, session.Id);
                sessionId = session.Id;
            }

            var agentResponse = await foundationaLLMService.GetFoundationaLLMResponse(
                new FoundationaLLMRequestModel
                {
                    UserPrompt = turnContext.Activity.Text,
                    SessionId = sessionId,
                    AgentName = "FoundationaLLM"
                }
            );
            await turnContext.SendActivityAsync(MessageFactory.Text(agentResponse.Text, agentResponse.Text), cancellationToken);
        }

        protected override async Task OnMembersAddedAsync(IList<ChannelAccount> membersAdded, ITurnContext<IConversationUpdateActivity> turnContext, CancellationToken cancellationToken)
        {
            var welcomeText = "Hello and welcome!";
            
            foreach (var member in membersAdded)
            {
                if (member.Id != turnContext.Activity.Recipient.Id)
                    await turnContext.SendActivityAsync(MessageFactory.Text(welcomeText, welcomeText), cancellationToken);
            }
        }
    }
}
