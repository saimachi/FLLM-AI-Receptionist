﻿using Receptionist.Bot.Models;

namespace Receptionist.Bot.Interfaces
{
    public interface IFoundationaLLMService
    {
        Task<SessionResponseModel> CreateSession();
    }
}
