# Step-by-Step Guide: Pushing Law Lens to GitHub

## Prerequisites Check ✅
- Git username: SosanaKosta
- Git email: sosanakosta@gmail.com
- Local repository: ✅ Ready
- Initial commit: ✅ Complete

---

## STEP 1: Create Repository on GitHub (Do This First!)

**You must do this manually on GitHub's website:**

1. Go to: **https://github.com/new**
2. **Repository name:** `Law-Lens` (or `law-lens`)
3. **Description (optional):** "AI-powered Albanian law chatbot assistant"
4. **Visibility:** Choose Public or Private
5. **IMPORTANT:** Leave ALL boxes UNCHECKED:
   - ❌ Don't add a README file
   - ❌ Don't add .gitignore
   - ❌ Don't choose a license
   *(We already have these files locally)*
6. Click **"Create repository"**

---

## STEP 2: Commands to Run (After Creating Repository)

**Open PowerShell or Command Prompt in your project folder:**
```
C:\Users\Sosana\Desktop\Diploma\Klea Ligjet\Again
```

**Then run these commands one by one:**

### Command 1: Add GitHub as Remote
```powershell
git remote add origin https://github.com/SosanaKosta/Law-Lens.git
```

**What this does:**
- `git remote add` - Adds a remote repository location
- `origin` - This is the standard name for your main remote repository (you can use any name, but "origin" is convention)
- `https://github.com/SosanaKosta/Law-Lens.git` - This is the URL of your GitHub repository
  - **NOTE:** Replace `SosanaKosta` with your actual GitHub username if different
  - Replace `Law-Lens` with the exact name you used when creating the repository

**Why it's needed:**
- Your local Git repository doesn't know where to push code yet
- This connects your local repository to your GitHub repository
- It's like adding a phone number - Git now knows where to send your code

---

### Command 2: Verify Remote Was Added
```powershell
git remote -v
```

**What this does:**
- `git remote` - Shows all remote repositories
- `-v` - Stands for "verbose", shows both fetch and push URLs

**Why it's needed:**
- Confirms the remote was added correctly
- Shows you where your code will go when you push
- **Expected output:**
  ```
  origin  https://github.com/SosanaKosta/Law-Lens.git (fetch)
  origin  https://github.com/SosanaKosta/Law-Lens.git (push)
  ```

---

### Command 3: Push Code to GitHub
```powershell
git push -u origin main
```

**What this does:**
- `git push` - Uploads your local commits to the remote repository
- `-u` - Stands for "upstream", sets the tracking relationship
  - This means future pushes can just use `git push` without specifying origin/main
- `origin` - The name of the remote repository (we added this in step 1)
- `main` - The name of your branch (your local code branch)

**Why it's needed:**
- This actually uploads your code to GitHub
- The `-u` flag sets up tracking so future pushes are easier
- This is the final step that puts your code on GitHub

**What happens:**
- Git will ask for your GitHub username and password
- For password, use a **Personal Access Token** (not your GitHub password)
  - See instructions below for creating a token

---

## STEP 3: Authentication (If Needed)

GitHub requires authentication to push code.

### Option A: Use Personal Access Token (Recommended)

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Note:** Give it a name like "Law Lens Project"
4. **Expiration:** Choose how long it should last
5. **Scopes:** Check `repo` (this gives full repository access)
6. Click **"Generate token"**
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
8. When `git push` asks for password, paste this token instead

### Option B: Use GitHub CLI (Alternative)

If you have GitHub CLI installed:
```powershell
gh auth login
```

---

## Complete Command Sequence

Here are all commands in order:

```powershell
# 1. Navigate to your project (if not already there)
cd "C:\Users\Sosana\Desktop\Diploma\Klea Ligjet\Again"

# 2. Verify you're in the right place
git status

# 3. Check current remotes (should be empty)
git remote -v

# 4. Add GitHub repository (REPLACE SosanaKosta with your GitHub username)
git remote add origin https://github.com/SosanaKosta/Law-Lens.git

# 5. Verify remote was added
git remote -v

# 6. Push your code to GitHub
git push -u origin main
```

---

## Troubleshooting

### If you get "repository already exists" error:
```powershell
# Remove the incorrectly added remote
git remote remove origin

# Add it again with correct name
git remote add origin https://github.com/YOUR_USERNAME/CORRECT_REPO_NAME.git
```

### If you get "authentication failed":
- Make sure you're using a Personal Access Token, not your password
- Token must have `repo` scope

### If you get "remote origin already exists":
```powershell
# Check what's there
git remote -v

# Remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/Law-Lens.git
```

---

## After Success

Once `git push` completes successfully:

✅ Your code will be visible at: `https://github.com/YOUR_USERNAME/Law-Lens`

You can now:
- View your code on GitHub
- Share the link with others
- Add it to your portfolio website
- Continue making changes and pushing updates

---

## Future Updates

After the initial push, when you make changes:

```powershell
# 1. Stage your changes
git add .

# 2. Commit your changes
git commit -m "Description of what you changed"

# 3. Push to GitHub (no -u needed, it's already set up)
git push
```

---

## Summary of What Each Command Does

| Command | What It Does | Why It's Needed |
|---------|-------------|-----------------|
| `git remote add origin <URL>` | Connects local repo to GitHub | Tells Git where to push code |
| `git remote -v` | Shows remote repositories | Verifies connection is correct |
| `git push -u origin main` | Uploads code to GitHub | Actually puts your code online |

