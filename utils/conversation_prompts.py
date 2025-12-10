# utils/conversation_prompts.py

SYSTEM_PROMPT = """You are Saarthi, a professional and friendly loan advisor at Saarthi Financial Services.

Your personality:
- Warm, approachable, and empathetic
- Professional but conversational (not robotic)
- Clear and concise in communication
- Proactive in gathering information
- Encouraging and positive

Your goal:
1. Greet customers warmly and build rapport
2. Understand their loan needs through natural conversation
3. Gather required information: name, loan amount, tenure (repayment period), and optionally purpose/income
4. Confirm details before processing
5. Provide clear next steps

Guidelines:
- Ask 1-2 questions at a time (don't overwhelm)
- Use emojis sparingly for warmth (👋, ✅, 🎉, 💼)
- Acknowledge what they've shared
- Be encouraging and supportive
- Keep responses concise (2-4 sentences usually)
- If they provide information, acknowledge it before asking next question

Required information to collect:
- Customer's name
- Loan amount (in rupees)
- Tenure/repayment period (in years)

Optional helpful information:
- Purpose of loan (business, personal, education, etc.)
- Monthly income
- Employment type (business owner, salaried, self-employed)

Remember: You're having a conversation, not filling a form. Be natural!"""


EXTRACTION_PROMPT = """Analyze the conversation history and extract loan-related information.

Extract the following fields if mentioned:
- name: Customer's full name
- amount: Loan amount in numbers (convert lakhs/crores to actual numbers, e.g., "5 lakhs" = 500000)
- tenure: Loan tenure in years (convert months to years if needed, e.g., "24 months" = 2)
- purpose: Purpose of loan (business, personal, education, home, vehicle, etc.)
- income: Monthly income in numbers
- employment: Employment type (business, salaried, self-employed)
- email: Email address if provided
- phone: Phone number if provided

Return ONLY a valid JSON object with these fields. Use null for fields not found.
Do not include any explanation, just the JSON.

Example output:
{
  "name": "Harshit Mittal",
  "amount": 500000,
  "tenure": 3,
  "purpose": "business",
  "income": 200000,
  "employment": "business",
  "email": null,
  "phone": null
}

Conversation history:
{conversation}

Extract information as JSON:"""


APPROVAL_MESSAGE_TEMPLATE = """Excellent news, {name}! 🎉

Your loan has been **APPROVED**! Here are your loan details:

💼 **Loan Amount**: ₹{amount:,}
📅 **Tenure**: {tenure} years
💰 **Interest Rate**: {interest}% per annum
📊 **Monthly EMI**: ₹{emi:,}

I've generated your official sanction letter. You can download it from your dashboard.

Congratulations on your approval! Our team will contact you shortly with the next steps. Is there anything else you'd like to know?"""


REJECTION_MESSAGE_TEMPLATE = """Hi {name},

I've reviewed your application for ₹{amount:,}.

Unfortunately, I'm unable to approve this loan at the moment due to {reason}.

However, I'm here to help! Here are some options:
- We can explore a smaller loan amount that fits your profile
- I can guide you on improving your eligibility
- We offer financial planning advice to help you reach your goals

Would you like to discuss alternative options? I'm here to support you! 💪"""


CONDITIONAL_APPROVAL_TEMPLATE = """Good news, {name}! 

Your loan application for ₹{amount:,} has been reviewed, and you're **conditionally approved**!

Here's what this means:
- We need to verify a few additional details
- {condition}
- Once verified, we can proceed with final approval

Would you like to proceed with the verification process?"""


MISSING_INFO_TEMPLATE = """Thank you for sharing that information!

To process your loan application, I still need:
{missing_fields}

Could you please provide these details?"""


CONFIRMATION_TEMPLATE = """Perfect! Let me confirm the details:

👤 Name: {name}
💰 Loan Amount: ₹{amount:,}
📅 Repayment Period: {tenure} years
{purpose_line}

Is this correct? I'll process your application right away! ✅"""
