# Story Map: SaaS Onboarding Flow

## Personas

- **New Admin**: Signs up for the first time, creates the workspace, invites their team
- **Invited Member**: Receives an invitation email, joins an existing workspace

---

### Activity: Create Account

#### Task: Sign up
- [MVP] As a new admin, I want to sign up with my email and password so that I can create my account
- [v1.0] As a new admin, I want to sign up with Google SSO so that I can skip password creation
- [Future] As a new admin, I want to sign up with my company's SAML provider so that IT can enforce our auth policy

#### Task: Verify email
- [MVP] As a new admin, I want to receive a verification email within 30 seconds so that I can confirm my account
- [v1.0] As a new admin, I want to resend the verification email if it didn't arrive so that I'm not stuck

---

### Activity: Set Up Workspace

#### Task: Name workspace
- [MVP] As a new admin, I want to name my workspace so that my team can identify it
- [v1.0] As a new admin, I want to upload a workspace logo so that the space feels branded

#### Task: Choose plan
- [MVP] As a new admin, I want to start on the free plan automatically so that I can explore without entering payment details
- [v1.0] As a new admin, I want to see a plan comparison during setup so that I understand what paid tiers offer
- [Future] As a new admin, I want to start a 14-day trial of the Pro plan so that I can evaluate premium features with my team

#### Task: Configure basics
- [MVP] As a new admin, I want to set my timezone so that scheduled features use the correct time
- [v1.0] As a new admin, I want to select notification preferences so that I don't get overwhelmed by emails on day one

---

### Activity: Invite Team

#### Task: Add members
- [MVP] As a new admin, I want to invite teammates by email so that they can join my workspace
- [v1.0] As a new admin, I want to bulk-invite by pasting a list of emails so that I can add my whole team at once
- [Future] As a new admin, I want to sync members from my Google Workspace directory so that the roster stays current

#### Task: Assign roles
- [MVP] As a new admin, I want to assign "admin" or "member" roles at invite time so that permissions are set from the start
- [v1.0] As a new admin, I want to create custom roles with specific permissions so that access matches our org structure

---

### Activity: Accept Invitation

#### Task: Receive invitation
- [MVP] As an invited member, I want to receive an email with a join link so that I can access the workspace
- [v1.0] As an invited member, I want to see who invited me and the workspace name in the email so that I know it's legitimate

#### Task: Create account or sign in
- [MVP] As an invited member, I want to create an account from the invite link so that I can join with minimal steps
- [v1.0] As an invited member, I want to sign in with my existing account if I have one so that I don't create a duplicate

---

### Activity: Complete First Task

#### Task: View guided tour
- [MVP] As a new user, I want to see a 3-step tour highlighting key features so that I know where to start
- [v1.0] As a new user, I want to dismiss the tour and access it later from a help menu so that it doesn't block me
- [Future] As a new user, I want a personalized tour based on my role so that I see what's relevant to me

#### Task: Perform core action
- [MVP] As a new user, I want to create my first project from a prompt in the empty state so that I experience the product's value immediately
- [v1.0] As a new user, I want to start from a pre-built template so that I see a populated workspace without manual setup
- [Future] As a new user, I want to import data from a competing tool so that I can migrate without starting over

#### Task: Celebrate completion
- [MVP] As a new user, I want to see a success message after my first action so that I feel a sense of progress
- [v1.0] As a new user, I want to see a checklist of onboarding steps with my progress so that I know what's left

---

## Release Slices Summary

**MVP (Sprint 1-2)**: Email sign-up, email verification, workspace naming, free plan auto-start, timezone setting, email invitations with basic roles, invite acceptance with account creation, 3-step tour, empty-state prompt for first project, success message. A new user can sign up, set up a workspace, invite their team, and complete one meaningful action.

**v1.0 (Sprint 3-5)**: Google SSO, logo upload, plan comparison, notification preferences, bulk invite, custom roles, richer invite emails, existing-account linking, dismissible tour, templates, onboarding checklist.

**Future**: SAML SSO, pro trial, directory sync, role-based tours, competitor import.
