"""Browser smoke tests for the static project page.

Start a local server, then run:
    python3 scripts/check_site.py --url http://127.0.0.1:8000

Requires Playwright and its Chromium browser. Screenshots go to test-results/.
Use --render-social to also refresh the social-preview.png asset.
"""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--render-social", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = root / "test-results"
    output.mkdir(exist_ok=True)
    url = args.url.rstrip("/")
    errors = []
    failures = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 1050}, reduced_motion="reduce")
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.on("response", lambda response: failures.append(f"{response.status} {response.url}") if response.status >= 400 else None)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        assert page.evaluate("[...document.fonts].every(font => font.status !== 'error')"), (page.evaluate("[...document.fonts].map(font => [font.family, font.status])"), errors)
        assert page.locator("h1").count() == 1
        assert page.locator(".resource-button[disabled]").count() == 2
        assert page.locator("#composition-explorer").is_visible()
        assert "Lato" in page.locator("h1").evaluate("e => getComputedStyle(e).fontFamily")
        assert page.locator("main > section").evaluate_all("sections => sections.slice(0, 2).map(section => section.id)") == ["top", "results"]
        assert page.locator("#top .eyebrow").count() == 0
        assert page.locator(".scope-section").count() == 0
        assert page.locator("#search-title").inner_text() == "Task-Level Successive Halving"
        assert "preliminary evidence for our hypothesis" in page.locator("#search .section-heading").inner_text()
        assert "Compositions of multiple continual learning mechanisms make memory last longer." == page.locator("#teaser-title").inner_text()
        assert not page.locator("a[href]").evaluate_all("links => links.some(link => /\\.pdf(?:$|[?#])/i.test(link.getAttribute('href')))")
        assert not any(path.suffix.lower() == ".pdf" for path in root.rglob("*") if ".git" not in path.parts)

        # All in-page destinations and full-resolution PNG links must resolve.
        for link in page.locator('a[href^="#"]').all():
            target = link.get_attribute("href")
            assert page.locator(target).count() == 1, target
        for link in page.locator(".figure-link").all():
            assert context.request.get(f"{url}/{link.get_attribute('href')}").status == 200

        # Check every checkbox combination, including output ranks and uncertainties.
        mechanisms = ["si", "sd", "replay", "merge"]
        dataset_ids = ["symbol", "llm", "real"]
        results = page.evaluate("COMPOSE_CL_RESULTS")
        assert len(results) == 16
        assert results["si_sd_replay_merge"]["mean"] == [18.5, 41.8, 44.3]
        assert results["vanilla"]["mean"] == [1.0, 1.4, 1.3]
        for bits in range(16):
            active = []
            for index, mechanism in enumerate(mechanisms):
                selected = bool(bits & (1 << index))
                page.locator(f'input[value="{mechanism}"]').set_checked(selected)
                if selected:
                    active.append(mechanism)
            key = "_".join(active) or "vanilla"
            for index, dataset in enumerate(dataset_ids):
                expected = results[key]["mean"][index]
                rank = 1 + sum(item["mean"][index] > expected for item in results.values())
                assert page.locator(f"#{dataset}-value").inner_text() == f"{expected:.1f}"
                assert page.locator(f"#{dataset}-std").inner_text() == f"{results[key]['std'][index]:.1f}"
                assert page.locator(f"#{dataset}-rank").inner_text() == f"Rank {rank} of 16"
        page.locator("#reset-composition").click()
        assert page.locator('input[name="mechanism"]:checked').count() == 4
        page.locator('input[value="si"]').focus()
        page.keyboard.press("Space")
        assert not page.locator('input[value="si"]').is_checked()
        page.keyboard.press("Space")

        # The fallback selects text and explains keyboard copying if clipboard access fails.
        page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:undefined})")
        page.locator("#copy-bibtex").click()
        assert "Ctrl+C" in page.locator("#copy-status").inner_text()
        assert "@article" in page.evaluate("window.getSelection().toString()")
        page.evaluate("window.getSelection().removeAllRanges()")
        page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:async text=>{window.copiedCitation=text}}})")
        page.locator("#copy-bibtex").click()
        page.wait_for_function("document.getElementById('copy-status').textContent === 'BibTeX copied to clipboard.'")
        assert "zhang2026continual" in page.evaluate("window.copiedCitation")
        assert page.evaluate("window.copiedCitation.startsWith('@article{')")
        assert not page.evaluate("/^\\s*url\\s*=/mi.test(window.copiedCitation)")

        for width in (1440, 1024, 768, 390, 320):
            page.set_viewport_size({"width": width, "height": 1050 if width > 640 else 844})
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(100)
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Horizontal overflow at {width}px"
            if width in (1440, 390):
                page.screenshot(path=str(output / f"page-{width}.png"), full_page=True)
                page.screenshot(path=str(output / f"hero-{width}.png"))
                page.locator("#composition-explorer").screenshot(path=str(output / f"explorer-{width}.png"))
        page.set_viewport_size({"width": 1440, "height": 1050})
        page.locator("#method").screenshot(path=str(output / "method.png"))
        page.locator("#search").screenshot(path=str(output / "search.png"))
        for image in page.locator("img").all():
            assert image.evaluate("e => e.complete && e.naturalWidth > 0"), image.get_attribute("src")

        no_js = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844})
        static_page = no_js.new_page()
        static_page.goto(url, wait_until="networkidle")
        assert not static_page.locator("#composition-explorer").is_visible()
        assert static_page.locator("#abstract").is_visible()
        assert static_page.locator(".factorial-figure").is_visible()
        assert static_page.locator("#bibtex-code").is_visible()
        no_js.close()

        if args.render_social:
            social = context.new_page()
            social.set_viewport_size({"width": 1200, "height": 630})
            social.goto(f"{url}/scripts/social-preview.html", wait_until="networkidle")
            social.evaluate("document.fonts.ready")
            assert social.evaluate("document.documentElement.scrollHeight <= 630")
            social.screenshot(path=str(root / "static" / "images" / "social-preview.png"))
        browser.close()

    assert not errors, errors
    assert not failures, failures
    print("PASS: all 16 combinations, keyboard input, citation copying and fallback, local links, images, fonts, no-JavaScript content, and five viewport sizes.")
    print(f"Screenshots: {output}")


if __name__ == "__main__":
    main()
