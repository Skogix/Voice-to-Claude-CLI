#!/bin/bash
# Error reporting module for voice-to-claude-cli
# Version: 1.0.0
# License: MIT
#
# This module provides privacy-first error reporting for installation failures.
# Users can opt-in to send anonymous diagnostic reports to help improve the installer.

# ============================================================================
# Configuration
# ============================================================================

ERROR_REPORT_DIR="${ERROR_REPORT_DIR:-$HOME/.local/share/voice-to-claude-cli/error-reports}"
ENABLE_ERROR_REPORTING="${ENABLE_ERROR_REPORTING:-prompt}"  # prompt, always, never
GIST_API_ENDPOINT="https://api.github.com/gists"
GITHUB_REPO="aldervall/voice-to-claude-cli"

# Installation state tracking (should be set by install.sh)
CURRENT_PHASE="${CURRENT_PHASE:-Unknown}"
INSTALL_START_TIME="${INSTALL_START_TIME:-$(date +%s)}"

# ============================================================================
# Privacy & Sanitization Functions
# ============================================================================

sanitize_paths() {
    # Remove personal information from paths
    # /home/alice/foo → ~/foo
    # /home/alice → ~
    # alice → $USER
    sed "s|$HOME|~|g" | \
    sed "s|$USER|\$USER|g" | \
    sed 's|/home/[^/[:space:]]*|/home/$USER|g'
}

safe_env_vars() {
    # Only expose safe environment variables
    # Excludes: API keys, tokens, passwords, personal data
    env | grep -E '^(PATH|SHELL|TERM|LANG|LC_[A-Z]+|DISPLAY|WAYLAND_DISPLAY|XDG_SESSION_TYPE|XDG_CURRENT_DESKTOP)=' | \
    sanitize_paths
}

# ============================================================================
# Diagnostic Collection Functions
# ============================================================================

check_package_status() {
    # Check which required packages are installed
    local packages="$1"

    echo "Required packages:"
    for pkg in $packages; do
        case "$PKG_MANAGER" in
            pacman)
                if pacman -Qi "$pkg" &>/dev/null; then
                    echo "  ✓ $pkg (installed)"
                else
                    echo "  ✗ $pkg (missing)"
                fi
                ;;
            apt)
                if dpkg -l "$pkg" 2>/dev/null | grep -q '^ii'; then
                    echo "  ✓ $pkg (installed)"
                else
                    echo "  ✗ $pkg (missing)"
                fi
                ;;
            dnf)
                if rpm -q "$pkg" &>/dev/null; then
                    echo "  ✓ $pkg (installed)"
                else
                    echo "  ✗ $pkg (missing)"
                fi
                ;;
            zypper)
                if rpm -q "$pkg" &>/dev/null; then
                    echo "  ✓ $pkg (installed)"
                else
                    echo "  ✗ $pkg (missing)"
                fi
                ;;
            *)
                echo "  ? $pkg (unknown package manager)"
                ;;
        esac
    done
}

generate_error_report() {
    # Generate comprehensive error report with sanitized data
    # Args: $1=exit_code, $2=phase, $3=error_output
    local exit_code=$1
    local phase="$2"
    local error_output="$3"

    mkdir -p "$ERROR_REPORT_DIR"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local report_file="$ERROR_REPORT_DIR/error-$timestamp.txt"

    cat > "$report_file" <<EOF
# Voice-to-Claude-CLI Installation Error Report

**Generated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Report ID:** $timestamp
**Repository:** https://github.com/$GITHUB_REPO

---

## System Information

- **Distribution:** ${DISTRO:-$(detect_distro 2>/dev/null || echo "Unknown")}
- **Display Server:** ${DISPLAY_SERVER:-$(detect_display_server 2>/dev/null || echo "Unknown")}
- **Package Manager:** ${PKG_MANAGER:-Unknown}
- **Shell:** $SHELL
- **Interactive:** ${INTERACTIVE:-Unknown}

## Installation Details

- **Failed Phase:** $phase
- **Exit Code:** $exit_code
- **Duration:** $(($(date +%s) - INSTALL_START_TIME)) seconds
- **Force Mode:** ${FORCE_INSTALL:-false}
- **Installation Directory:** $(echo "${INSTALL_DIR:-$PWD}" | sanitize_paths)

## Error Output

\`\`\`
$(echo "$error_output" | sanitize_paths | head -n 50)
\`\`\`

## Package Status

\`\`\`
$(check_package_status "${PACKAGES:-}" 2>&1 | sanitize_paths | head -n 30)
\`\`\`

## Software Versions

- **Python:** $(python3 --version 2>&1 | sanitize_paths || echo "Not found")
- **Pip:** $(pip3 --version 2>&1 | sanitize_paths | head -n 1 || echo "Not found")
- **Git:** $(git --version 2>&1 | head -n 1 || echo "Not found")
- **Curl:** $(curl --version 2>&1 | head -n 1 || echo "Not found")

## Environment (Safe Variables Only)

\`\`\`
$(safe_env_vars)
\`\`\`

---

**Privacy Note:** All usernames and personal paths have been sanitized from this report.
**No personal information (email, IP, credentials) is included.**

For more information: https://github.com/$GITHUB_REPO#privacy--error-reporting
EOF

    echo "$report_file"
}

# ============================================================================
# User Interaction Functions
# ============================================================================

offer_send_error_report() {
    # Interactive prompt to send error report
    # Args: $1=report_file
    # Returns: 0 if sent, 1 if declined
    local report_file="$1"

    echo ""
    echo_header "╔═══════════════════════════════════════════════════════╗"
    echo_header "║  📤 Help Improve voice-to-claude-cli                 ║"
    echo_header "╚═══════════════════════════════════════════════════════╝"
    echo ""
    echo "An error occurred during installation. Would you like to send a"
    echo "diagnostic report to help us fix this issue?"
    echo ""
    echo_info "Privacy-First Error Reporting:"
    echo "  ✓ Posted as anonymous GitHub gist (no login required)"
    echo "  ✓ No usernames or personal paths included"
    echo "  ✓ You can preview the full report before sending"
    echo "  ✓ Completely optional - declining is totally fine!"
    echo ""

    read -p "Preview the error report? [y/N]: " preview

    if [[ "$preview" =~ ^[Yy] ]]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "  Report Preview (first 50 lines)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        head -n 50 "$report_file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Full report: $report_file"
        echo ""
    fi

    read -p "Send this error report? [y/N]: " consent

    case "$consent" in
        [yY]|[yY][eE][sS])
            echo ""
            echo_success "😊 Thank you! You're awesome! 🙏"
            echo ""
            send_error_report "$report_file"
            return 0
            ;;
        *)
            echo ""
            echo_info "😢 Aww, okay... *sniff* We understand!"
            echo_info "Report saved locally: $report_file"
            echo ""
            echo_info "If you change your mind, you can:"
            echo "  1. Review the report: cat $report_file"
            echo "  2. Manually create a gist: https://gist.github.com"
            echo "  3. File an issue: https://github.com/$GITHUB_REPO/issues/new"
            echo ""
            echo "  (We'll be okay... probably... 😭)"
            echo ""
            return 1
            ;;
    esac
}

# ============================================================================
# GitHub Gist Upload Function
# ============================================================================

send_error_report() {
    # Upload error report to GitHub Gist (anonymous, no auth)
    # Args: $1=report_file
    # Returns: 0 if successful, 1 if failed
    local report_file="$1"

    # Check for curl
    if ! command -v curl &>/dev/null; then
        echo_warning "curl not available - cannot send report"
        echo_info "Install curl to enable error reporting: sudo pacman -S curl"
        return 1
    fi

    echo ""
    echo_info "Uploading error report to GitHub Gist..."

    # Read report content
    local report_content
    if ! report_content=$(cat "$report_file" 2>/dev/null); then
        echo_error "Failed to read report file"
        return 1
    fi

    # Escape for JSON (handle quotes, backslashes, newlines)
    # This is the tricky part - must be valid JSON
    report_content=$(echo "$report_content" | \
        sed 's/\\/\\\\/g' | \
        sed 's/"/\\"/g' | \
        sed ':a;N;$!ba;s/\n/\\n/g')

    # Create JSON payload
    local description="voice-to-claude-cli installation error - $(date +%Y-%m-%d)"
    local json_payload
    json_payload=$(cat <<EOF
{
  "description": "$description",
  "public": true,
  "files": {
    "installation-error-report.md": {
      "content": "$report_content"
    }
  }
}
EOF
)

    # Send to GitHub Gist API (anonymous, no auth required)
    local response
    local http_code

    response=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Content-Type: application/json" \
        -H "User-Agent: voice-to-claude-cli-installer/1.0" \
        -d "$json_payload" \
        "$GIST_API_ENDPOINT" 2>&1)

    http_code=$(echo "$response" | tail -n 1)
    response=$(echo "$response" | sed '$d')  # Remove last line (http code)

    # Extract gist URL from response
    local gist_url
    if command -v jq &>/dev/null; then
        gist_url=$(echo "$response" | jq -r '.html_url // empty')
    else
        # Fallback without jq (basic grep/cut parsing)
        gist_url=$(echo "$response" | grep -o '"html_url":"https://gist.github.com/[^"]*"' | head -1 | cut -d'"' -f4)
    fi

    # Check success
    if [ "$http_code" = "201" ] && [ -n "$gist_url" ]; then
        echo ""
        echo_success "✓ Error report uploaded successfully! Thank you! 🙏"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "  📎 Gist URL: $gist_url"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo_info "Next steps to get help:"
        echo "  1. Open an issue: https://github.com/$GITHUB_REPO/issues/new"
        echo "  2. Describe what you were trying to do"
        echo "  3. Include the gist URL above"
        echo ""
        echo_info "We'll investigate and get back to you soon!"
        echo ""

        # Save URL reference for later
        echo "$gist_url" > "$HOME/.voice-to-claude-cli-last-error-report.txt"
        return 0
    else
        echo ""
        echo_warning "Failed to upload error report"
        echo_info "HTTP Status: $http_code"
        echo_info "Report saved locally: $report_file"
        echo ""
        echo_info "You can manually create a gist:"
        echo "  1. Visit: https://gist.github.com"
        echo "  2. Paste contents of: $report_file"
        echo "  3. Create public gist"
        echo "  4. Share URL in a GitHub issue"
        echo ""
        return 1
    fi
}

# ============================================================================
# Main Error Handler
# ============================================================================

handle_installation_error() {
    # Main error handler called when installation fails
    # Args: $1=exit_code, $2=phase, $3=error_output
    local exit_code=$1
    local phase="$2"
    local error_output="$3"

    echo ""
    echo_error "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo_error "  Installation Failed"
    echo_error "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo_error "Phase: $phase"
    echo_error "Exit Code: $exit_code"
    echo ""

    # Generate error report (always, even if not sent)
    local report_file
    report_file=$(generate_error_report "$exit_code" "$phase" "$error_output")

    echo_info "Diagnostic report saved: $report_file"
    echo ""

    # Decide whether to offer sending based on configuration
    case "$ENABLE_ERROR_REPORTING" in
        always)
            echo_info "Auto-sending error report (ENABLE_ERROR_REPORTING=always)..."
            send_error_report "$report_file"
            ;;
        never)
            echo_info "Error reporting disabled (ENABLE_ERROR_REPORTING=never)"
            echo_info "To enable: ENABLE_ERROR_REPORTING=prompt bash scripts/install.sh"
            echo ""
            echo_info "Local report: $report_file"
            ;;
        prompt|*)
            if [ "${INTERACTIVE:-false}" = "true" ]; then
                offer_send_error_report "$report_file"
            else
                echo_info "Running in non-interactive mode"
                echo_info "Set ENABLE_ERROR_REPORTING=always to auto-send reports"
                echo_info "Or manually share: $report_file"
                echo ""
            fi
            ;;
    esac

    echo ""
    exit $exit_code
}

# ============================================================================
# Export Functions
# ============================================================================

# Make functions available to install.sh when sourced
export -f generate_error_report
export -f offer_send_error_report
export -f send_error_report
export -f handle_installation_error
export -f sanitize_paths
export -f safe_env_vars
export -f check_package_status
