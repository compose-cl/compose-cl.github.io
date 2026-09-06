"""Browser checks for recorded TSH decisions and playback controls."""


def check_tsh(page, output):
    root = page.locator("#tsh-explorer")
    root.scroll_into_view_if_needed()
    assert root.is_visible()
    assert not page.locator("#tsh-fallback").is_visible()
    assert page.locator("#tsh-matrix .tsh-candidates").count() == 16
    assert page.locator("#tsh-matrix .tsh-dot").count() == 90
    assert page.locator("#tsh-play").inner_text() == "Play", "Reduced motion must disable autoplay"
    data = page.evaluate("COMPOSE_CL_TSH")
    assert data["seeds"] == [41, 42, 43]

    for dataset, record in data["datasets"].items():
        page.locator(f'[data-tsh-dataset="{dataset}"]').click()
        assert page.locator(f'[data-tsh-dataset="{dataset}"]').get_attribute("aria-pressed") == "true"
        for task in (0, 9, 10, 19, 20, 49, 50, 99, 100, 20, 0):
            page.locator("#tsh-progress").evaluate("(e, value) => { e.value = value; e.dispatchEvent(new Event('input', {bubbles: true})); }", task)
            completed = [stage for stage in record["stages"] if stage["task"] <= task]
            expected = set(completed[-1]["survivors"] if completed else range(90))
            actual = page.locator("#tsh-matrix .tsh-dot:not(.is-eliminated)").evaluate_all("dots => dots.map(dot => Number(dot.dataset.candidate))")
            assert set(actual) == expected, (dataset, task)
            assert page.locator("#tsh-count").inner_text() == str(len(expected))
            assert page.locator("#tsh-task").inner_text() == str(task)
            assert page.locator("#tsh-play").inner_text() == "Play"
            assert "candidates remain" in page.locator("#tsh-progress").get_attribute("aria-valuetext")
            for cell in page.locator(".tsh-candidates").all():
                alive = cell.locator(".tsh-dot:not(.is-eliminated)").count()
                assert cell.locator(".tsh-cell-count strong").inner_text() == str(alive)
                assert f"{alive} of" in cell.get_attribute("aria-label")
            if dataset == "symbol_qa" and task in (0, 10, 20, 50, 100):
                root.screenshot(path=str(output / f"tsh-task-{task}.png"))

    # Dataset selection preserves the task position. Jump buttons and keyboard
    # controls pause playback, and reverse scrubbing restores eliminated methods.
    page.locator('[data-tsh-task="50"]').click()
    page.locator('[data-tsh-dataset="symbol_qa"]').click()
    assert page.locator("#tsh-task").inner_text() == "50"
    assert page.locator("#tsh-count").inner_text() == "10"
    slider = page.locator("#tsh-progress")
    slider.focus()
    page.keyboard.press("Home")
    assert page.locator("#tsh-count").inner_text() == "90"
    page.keyboard.press("ArrowRight")
    assert slider.input_value() == "1"
    page.keyboard.press("End")
    assert page.locator("#tsh-count").inner_text() == "10"
    page.locator('[data-tsh-task="20"]').click()
    page.set_viewport_size({"width": 390, "height": 844})
    root.screenshot(path=str(output / "tsh-mobile.png"))
    page.set_viewport_size({"width": 1440, "height": 1050})


def check_tsh_playback(browser, url, errors):
    context = browser.new_context(viewport={"width": 1440, "height": 1050}, reduced_motion="no-preference")
    page = context.new_page()
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.clock.install()
    page.goto(url, wait_until="networkidle")
    page.clock.run_for(2000)
    assert page.locator("#tsh-task").inner_text() == "0", "Do not autoplay offscreen"
    page.locator("#tsh-explorer").scroll_into_view_if_needed()
    page.wait_for_timeout(100)  # Allow the browser's intersection notification.
    page.clock.run_for(6000)
    assert int(page.locator("#tsh-task").inner_text()) >= 10
    assert page.locator("#tsh-count").inner_text() == "45"
    page.locator("#tsh-play").click()
    paused_at = page.locator("#tsh-task").inner_text()
    page.clock.run_for(2000)
    assert page.locator("#tsh-task").inner_text() == paused_at
    page.locator("#tsh-play").click()
    page.clock.run_for(17000)
    assert page.locator("#tsh-task").inner_text() == "100"
    assert page.locator("#tsh-count").inner_text() == "10"
    assert page.locator("#tsh-play").inner_text() == "Play", "Stop at task 100"
    page.locator("#tsh-restart").click()
    assert page.locator("#tsh-count").inner_text() == "90"
    page.clock.run_for(1000)
    assert int(page.locator("#tsh-task").inner_text()) > 0
    page.locator("#tsh-progress").evaluate("e => {e.value=50; e.dispatchEvent(new Event('input', {bubbles:true}));}")
    page.clock.run_for(2000)
    assert page.locator("#tsh-task").inner_text() == "50"
    assert page.locator("#tsh-play").inner_text() == "Play"
    page.locator("#tsh-play").click()
    page.evaluate("window.scrollTo({top:0, behavior:'instant'})")
    page.wait_for_timeout(100)
    page.clock.run_for(200)
    offscreen_at = page.locator("#tsh-task").inner_text()
    page.clock.run_for(2000)
    assert page.locator("#tsh-task").inner_text() == offscreen_at
    page.locator("#tsh-explorer").scroll_into_view_if_needed()
    page.wait_for_timeout(100)
    page.clock.run_for(1000)
    assert int(page.locator("#tsh-task").inner_text()) > int(offscreen_at)
    page.emulate_media(reduced_motion="reduce")
    page.wait_for_timeout(100)
    page.clock.run_for(100)
    assert page.locator("#tsh-play").inner_text() == "Play"
    # Explicit play is still allowed when reduced motion is enabled.
    page.locator("#tsh-play").click()
    page.clock.run_for(1000)
    assert page.locator("#tsh-play").inner_text() == "Pause"
    context.close()
