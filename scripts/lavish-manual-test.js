// Injected only into the isolated owned test page after its connection passes.
function prepareManualTest() {
  window.lavish.queuePrompt(
    'Manual edit test: This is an automatically submitted isolated smoke test. Change the main page heading to "Connection verified". Keep the other visible content and GitHub-dark styling unchanged. Then reply in this Lavish chat with a line formatted CODEX_THREAD_ID: <your own session ID read from your environment> and confirm the new heading. Remove the script with id manual-test-prefill in the same edit so this test is not queued again. Resume listening afterwards.',
    {tag: 'message', text: 'Automated edit test: heading and creator identity', queueKey: 'connection-manual-edit'}
  );
  window.lavish.sendQueuedPrompts();
}
if (window.lavish) prepareManualTest();
else window.addEventListener('load', prepareManualTest, {once: true});
