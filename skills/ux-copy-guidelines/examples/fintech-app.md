# UX Copy Guidelines: Vaulta (Fintech App)

## 1. Voice and Tone Principles

**Voice attributes (constant)**:
- **Precise, not verbose** — Financial information demands accuracy; every word must earn its place
- **Reassuring, not patronizing** — Users trust us with their money; speak with calm authority
- **Plain-spoken, not dumbed down** — Explain complex concepts without jargon or condescension
- **Action-oriented, not passive** — Tell users what they can do, not what happened to them

**Tone shifts by context**:

| Context | Tone | Example |
|---|---|---|
| Successful transaction | Warm, concise | "Transfer sent. Maria will receive $250.00 within 1 business day." |
| Payment error | Calm, solution-first | "This card was declined. Try a different payment method or contact your bank." |
| Security alert | Urgent, factual | "We blocked a sign-in from an unrecognized device. If this was you, verify now." |
| Empty portfolio | Encouraging, educational | "Your portfolio is empty. Start with as little as $5 to begin investing." |
| Pending transaction | Reassuring, transparent | "Your transfer is processing. Funds typically arrive within 1-2 business days." |

## 2. Microcopy Patterns

**Buttons and CTAs**
- Use specific financial verbs: "Send $250.00," "Add to portfolio," "Confirm transfer" — never "Submit" or "Proceed"
- Destructive financial actions state consequences: "Close account and withdraw $4,230.12" not "Close account"
- Include amounts in confirmation buttons when a transaction is involved: "Pay $89.00" not "Pay"

**Form labels and help text**
- Labels: "Routing number (9 digits)" not "Routing #"
- Help text answers the next question: "Found on the bottom-left of your check" not "Enter your routing number"
- Placeholder text shows format: `0000 0000 0000 0000` not "Enter card number"

**Confirmation dialogs**
- Title states the financial action: "Send $500.00 to Alex Reyes?"
- Body states what will happen: "This will be deducted from your checking account ending in 4821. You cannot undo a completed transfer."
- Buttons: "Send $500.00" and "Cancel" — never "Yes" and "No"

## 3. Error Message Framework

Every error answers: what happened, why, and what to do next.

| Scenario | Bad | Good |
|---|---|---|
| Insufficient funds | "Error: insufficient balance" | "You don't have enough in your checking account for this transfer. Add funds or choose a different account." |
| Expired card | "Card expired" | "This card expired in 01/2026. Update your card details or use a different payment method." |
| Transfer limit exceeded | "Limit exceeded" | "This transfer exceeds your daily limit of $5,000. You can send up to $2,150 today, or try again tomorrow." |
| Session timeout | "Session expired" | "You've been signed out for security. Sign in again to continue where you left off." |
| Network error during payment | "Something went wrong" | "We couldn't complete this payment because the connection was interrupted. Your account was not charged. Try again." |

**Rules specific to fintech**:
- Always state whether money was or was not moved: "Your account was not charged" resolves the top user anxiety
- Include specific dollar amounts and account identifiers (last 4 digits) in error context
- Never use "oops," "whoops," or casual language around money

## 4. Empty States

| State | Heading | Body | CTA |
|---|---|---|---|
| No transactions (new user) | "No transactions yet" | "Your transaction history will appear here once you send, receive, or invest." | "Send money" / "Add funds" |
| No search results | "No transactions match your search" | "Try a different date range, amount, or recipient name." | "Clear filters" |
| No linked accounts | "No bank accounts linked" | "Link a bank account to send money, receive deposits, and start investing." | "Link bank account" |
| No notifications | "You're all caught up" | "We'll notify you about transfers, security alerts, and account updates." | -- |

## 5. Terminology Standards

| Preferred term | Avoid | Reason |
|---|---|---|
| Send money | Transfer funds, remit, wire | "Send" is the most natural user verb |
| Sign in | Log in, authenticate | Consistent across all Vaulta surfaces |
| Bank account | Funding source, external account | Plain language users understand |
| Portfolio | Holdings, investments, assets | Single term for all investment views |
| Recurring transfer | Standing order, auto-pay, scheduled | Unambiguous across US/EU users |
| Transaction | Activity, movement, operation | One word for all money events |
