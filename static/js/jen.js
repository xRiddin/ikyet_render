
    const writeOutput = (data, converter) => {
		add_gpt_message_box(data.output);
		add_message(window.conversation_id, "assistant", data.output);
		const reportContainer = document.getElementById("message");
		const markdownOutput = converter.makeHtml(data.output);
		reportContainer.innerHTML += markdownOutput;
		prompt_lock = false;
		updateScroll();
	};