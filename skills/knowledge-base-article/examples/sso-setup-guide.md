# How to Set Up Single Sign-On (SSO) with Okta

## Overview

This article walks you through connecting your Okta organization to Vaultline so your team can sign in with their company credentials. Setup takes about 15 minutes and requires admin access to both Okta and Vaultline.

## Applies To

- **Vaultline plan:** Business or Enterprise
- **Role required:** Vaultline Organization Admin + Okta Super Admin
- **Supported protocol:** SAML 2.0
- **Not covered:** OIDC/OpenID Connect (see "Related Articles" below), SCIM provisioning

## Step-by-Step Solution

### Part A: Configure Okta

1. Sign in to your Okta admin console at `https://your-domain-admin.okta.com`.
2. Navigate to **Applications > Applications** in the left sidebar.
3. Click **Create App Integration**.
4. Select **SAML 2.0** and click **Next**.
   - You should see the "Create SAML Integration" wizard with a "General Settings" step.
5. Enter the following in General Settings:
   - **App name:** `Vaultline`
   - **App logo:** Upload the Vaultline logo (optional — download from `https://vaultline.io/brand/logo.png`)
   - Click **Next**.
6. In the "Configure SAML" step, enter these values:
   - **Single sign-on URL:** `https://auth.vaultline.io/saml/acs`
   - **Audience URI (SP Entity ID):** `https://auth.vaultline.io/saml/metadata`
   - **Name ID format:** `EmailAddress`
   - **Application username:** `Email`
7. Under **Attribute Statements**, add:
   - `firstName` -> `user.firstName`
   - `lastName` -> `user.lastName`
   - `email` -> `user.email`
8. Click **Next**, select "I'm an Okta customer adding an internal app," and click **Finish**.
   - You should land on the application's **Sign On** tab.
9. On the **Sign On** tab, click **View SAML setup instructions** (or scroll to the "SAML Signing Certificates" section).
10. Copy the following three values — you will need them in Part B:
    - **Identity Provider Single Sign-On URL**
    - **Identity Provider Issuer**
    - **X.509 Certificate** (click "Download certificate")

### Part B: Configure Vaultline

11. Sign in to Vaultline as an Organization Admin.
12. Navigate to **Settings > Security > Single Sign-On**.
13. Click **Configure SSO** and select **SAML 2.0**.
14. Paste the values from step 10:
    - **SSO URL:** paste the Identity Provider Single Sign-On URL
    - **Issuer URI:** paste the Identity Provider Issuer
    - **Certificate:** click **Upload** and select the downloaded `.cert` file
15. Under **SSO Enforcement**, choose one:
    - **Optional:** members can use SSO or email/password (recommended during testing)
    - **Required:** all members must use SSO (enable after confirming SSO works)
16. Click **Save Configuration**.
    - A green banner reading "SSO configuration saved" appears at the top of the page.

### Part C: Test the Connection

17. Click **Test SSO Connection** on the SSO settings page.
    - A new browser tab opens and redirects to your Okta login page.
18. Sign in with your Okta credentials.
    - IF successful: the tab displays "SSO connection verified" and redirects back to Vaultline.
    - IF it fails: see the Troubleshooting section below. Do not enable "Required" enforcement until the test passes.
19. After a successful test, assign the Vaultline app to users or groups in Okta:
    - In Okta, go to the Vaultline app > **Assignments** tab > **Assign** > select users or groups.

## Troubleshooting

| Still seeing this?                         | Try this                                                                                      |
|--------------------------------------------|-----------------------------------------------------------------------------------------------|
| "SAML response signature invalid"          | Re-download the X.509 certificate from Okta (step 10) and re-upload in Vaultline (step 14). Certificates rotate — ensure you have the active one. |
| "Audience URI mismatch"                    | Verify the Audience URI in Okta is exactly `https://auth.vaultline.io/saml/metadata` with no trailing slash. |
| Redirect loop after login                  | Clear browser cookies for `vaultline.io` and `okta.com`, then try again in an incognito window. |
| User gets "Account not found" after SSO    | The user's Okta email must match their Vaultline account email. Check under **Profile > Email** in Vaultline. |
| SSO works for admin but not other users    | Confirm users are assigned to the Vaultline app in Okta (**Applications > Vaultline > Assignments**). |
| "Certificate expired" error                | Generate a new signing certificate in Okta under **Sign On > SAML Signing Certificates > Generate New Certificate**, then re-upload in Vaultline. |
| All troubleshooting steps failed           | Contact Vaultline support at support@vaultline.io with: your Okta org URL, the error message, and a screenshot of your SAML configuration in Okta. |

## FAQs

**Can I use multiple identity providers?**
Enterprise plans support multiple IdPs. Go to **Settings > Security > SSO** and click **Add Provider** to configure a second SAML connection.

**What happens to existing email/password accounts when I enforce SSO?**
Existing users are prompted to sign in via SSO on their next login. Their accounts are linked automatically by email address. Passwords remain as a recovery fallback unless you disable password login separately.

**Does SSO affect API keys or service accounts?**
No. API keys and service accounts authenticate independently and are not subject to SSO enforcement.

**Can I require MFA in addition to SSO?**
MFA enforcement is handled in Okta. Configure MFA policies in your Okta org, and they apply when users authenticate through SSO.

## Related Articles

- [How to set up SSO with Azure AD (SAML)](../sso-azure-ad)
- [How to configure SSO with OpenID Connect (OIDC)](../sso-oidc-setup)
- [How to set up SCIM provisioning with Okta](../scim-okta-provisioning)
- [How to troubleshoot "Account not found" errors during SSO login](../sso-account-not-found)
