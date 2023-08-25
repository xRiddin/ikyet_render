const query = (obj) =>
	Object.keys(obj)
		.map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
		.join("&");
const url_prefix = document.querySelector('body').getAttribute('data-urlprefix')
const markdown = window.markdownit();
const message_box = document.getElementById(`messages`);
const message_input = document.getElementById(`message-input`);
const box_conversations = document.querySelector(`.top`);
const spinner = box_conversations.querySelector(".spinner");
const stop_generating = document.querySelector(`.stop-generating`);
const send_button = document.querySelector(`#send-button`);
const download_button = document.getElementById('download_button')
const user_image = `<img src="${url_prefix}/images/user.png" alt="User Avatar">`;
const gpt_image = `<img src="${url_prefix}/images/gpt.png" alt="GPT Avatar">`;
let prompt_lock = false;


hljs.addPlugin(new CopyButtonPlugin());

message_input.addEventListener("blur", () => {
	window.scrollTo(0, 0);
});

message_input.addEventListener("focus", () => {
	document.documentElement.scrollTop = document.documentElement.scrollHeight;
});
const delete_conversations = async () => {
	localStorage.clear();
	await new_conversation();
};

	/*if (message.length > 0) {
		message_input.value = ``;
		message_input.dispatchEvent(new Event("input"));
		await ask_gpt(message);

	}


const remove_cancel_button = async () => {
	stop_generating.classList.add(`stop-generating-hiding`);

	setTimeout(() => {
		stop_generating.classList.remove(`stop-generating-hiding`);
		stop_generating.classList.add(`stop-generating-hidden`);
	}, 300);
};
*/
const startResearch = () => {

		listenToSockEvents();
	};

	const listenToSockEvents=()=>{

		const {protocol, host, pathname} = window.location;
		const ws_uri = `${protocol === 'https:' ? 'wss:' : 'ws:'}//${host}/aidev`;
		const converter = new showdown.Converter();
		const socket = new WebSocket(ws_uri);
		window.token = message_id();

		socket.onmessage = (event) => {
			try {
				const data = JSON.parse(event.data);
				const responseText = data.output;
				console.log(data)
				console.log(responseText)
					if (data.type === 'logs') {
						addAgentResponse(data);
					} else if (data.type === 'output') {
						writeOutput(data, converter);
					} else if (data.type === 'link') {
						updateDownloadLink(data);
					}

			add_message(window.conversation_id, "assistant", responseText);
				prompt_lock = false;

			} catch(error){
				console.error("error parsing json:", error)
			}

		};

		socket.onopen = (event) => {
			try {
				if (message_input.value !== ``) {
					const input = message_input.value

					console.log(input)
					const web = document.getElementById("switch").checked
					const adv = document.getElementById("switch2").checked
					console.log(web)

					const requestData = {
						input: input,
						adv: adv,
						web: web,
					};
					console.log(requestData);

					socket.send(`${JSON.stringify(requestData)}`);
					add_user_message_box(input);
					add_message(window.conversation_id, "user", input);
					message_input.value = ``;

				} else {
					return
				}
			} catch (error){
				add_gpt_message_box("Error occurred check in console:", error)
			}
		}
	};
	const addAgentResponse = (data) => {
		const output = document.getElementById("messages");
		const text = markdown.render(data.output)
		console.log(text)
		output.innerHTML += '<div class="message">' + text + '</div>'
		output.scrollTop = output.scrollHeight;
		output.style.display = "block";
		prompt_lock = false
		updateScroll();
	};

	const writeOutput = (data, converter) => {
		add_gpt_message_box(data.output);
		add_message(window.conversation_id, "assistant", data.output);
		const reportContainer = document.getElementById("message");
		const markdownOutput = converter.makeHtml(data.output);
		reportContainer.innerHTML += markdownOutput;
		prompt_lock = false;
		updateScroll();
	};

	const updateDownloadLink = (data) => {
		const path = data.output;
		const downloadLink = document.getElementById("downloadLink");
		downloadLink.href = path;
	};

	const updateScroll = () => {
		window.scrollTo(0, document.body.scrollHeight);
	};
/*
async function openFileExplorer() {
	const fileInput = document.getElementById("fileInput");
	await fileInput.click();

}

async function processFile() {
	const fileList = document.getElementById("fileList");
	const fileInput = document.getElementById("fileInput");
	const files = fileInput.files;
	if (!files || files.length === 0) {
		alert("Please select a file.");
		return;
	}

	const formData = new FormData();
	for (let i = 0; i < files.length; i++) {
		formData.append("files", files[i]);
	}

	fetch("/upload", {
		method: "POST",
		body: formData,
	})
		.then((response) => response.text())
		.then((output) => {
			const outputBlock = document.getElementById("outputBlock");
			outputBlock.textContent = output;
			outputBlock.style.display = "block";
		})
		.catch((error) => console.error("Error:", error));
}
*/
 const add_user_message_box = (message) => {
	const messageDiv = document.createElement("div");
	messageDiv.classList.add("message");

	const avatarContainer = document.createElement("div");
	avatarContainer.classList.add("avatar-container");
	avatarContainer.innerHTML = user_image;

	const contentDiv = document.createElement("div");
	contentDiv.classList.add("content");
	contentDiv.id = `user_${token}`;
	contentDiv.innerText = message;

	messageDiv.appendChild(avatarContainer);
	messageDiv.appendChild(contentDiv);

	message_box.appendChild(messageDiv);
};

const add_gpt_message_box = (message) => {
	console.log(message)
	document.querySelectorAll(`code`).forEach((el) => {
				hljs.highlightElement(el);
			});
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");

    const avatarContainer = document.createElement("div");
    avatarContainer.classList.add("avatar-container");
    avatarContainer.innerHTML = gpt_image;

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("content");
    contentDiv.innerText = message;

    messageDiv.appendChild(avatarContainer);
    messageDiv.appendChild(contentDiv);
	message_box.appendChild(messageDiv);
    updateScroll();
};

/*
const decodeUnicode = (str) => {
	return str.replace(/\\u([a-fA-F0-9]{4})/g, function (match, grp) {
		return String.fromCharCode(parseInt(grp, 16));
	});
};
*/
const clear_conversations = async () => {
	const elements = box_conversations.childNodes;
	let index = elements.length;

	if (index > 0) {
		while (index--) {
			const element = elements[index];
			if (element.nodeType === Node.ELEMENT_NODE && element.tagName.toLowerCase() !== `button`) {
				box_conversations.removeChild(element);
			}
		}
	}
};

const clear_conversation = async () => {
	let messages = message_box.getElementsByTagName(`div`);

	while (messages.length > 0) {
		message_box.removeChild(messages[0]);
	}
};

const delete_conversation = async (conversation_id) => {
	localStorage.removeItem(`conversation:${conversation_id}`);

	if (window.conversation_id == conversation_id) {
		await new_conversation();
	}

	await load_conversations(20, 0, true);
};

const set_conversation = async (conversation_id) => {
	history.pushState({}, null, `${url_prefix}/chat/${conversation_id}`);
	window.conversation_id = conversation_id;

	await clear_conversation();
	await load_conversation(conversation_id);
	await load_conversations(20, 0, true);
};

const new_conversation = async () => {
	history.pushState({}, null, `${url_prefix}/aidev.html`);
	window.conversation_id = uuid();

	await clear_conversation();
	await load_conversations(20, 0, true);
};

const load_conversation = async (conversation_id) => {
	let conversation = await JSON.parse(localStorage.getItem(`conversation:${conversation_id}`));
	console.log(conversation, conversation_id);

	for (item of conversation.items) {
		if (is_assistant(item.role)) {
			message_box.innerHTML += load_gpt_message_box(item.content);
		} else {
			message_box.innerHTML += load_user_message_box(item.content);
		}
	}

	document.querySelectorAll(`code`).forEach((el) => {
		hljs.highlightElement(el);
	});

	message_box.scrollTo({top: message_box.scrollHeight, behavior: "smooth"});

	setTimeout(() => {
		message_box.scrollTop = message_box.scrollHeight;
	}, 500);
};

const load_user_message_box = (content) => {
	const messageDiv = document.createElement("div");
	messageDiv.classList.add("message");

	const avatarContainer = document.createElement("div");
	avatarContainer.classList.add("avatar-container");
	avatarContainer.innerHTML = user_image;

	const contentDiv = document.createElement("div");
	contentDiv.classList.add("content");
	contentDiv.innerText = content;

	messageDiv.appendChild(avatarContainer);
	messageDiv.appendChild(contentDiv);

	return messageDiv.outerHTML;
};

const load_gpt_message_box = (content) => {
	return `
            <div class="message">
                <div class="avatar-container">
                    ${gpt_image}
                </div>
                <div class="content">
                    ${markdown.render(content)}
                </div>
            </div>
        `;
};

const is_assistant = (role) => {
	return role == "assistant";
};
/*
const get_conversation = async (conversation_id) => {
	let conversation = await JSON.parse(localStorage.getItem(`conversation:${conversation_id}`));
	return conversation.items;
};

const add_conversation = async (conversation_id, title) => {
	if (localStorage.getItem(`conversation:${conversation_id}`) == null) {
		localStorage.setItem(
			`conversation:${conversation_id}`,
			JSON.stringify({
				id: conversation_id,
				title: title,
				items: [],
			})
		);
	}
};
*/
const add_message = async (conversation_id, role, content) => {
	before_adding = JSON.parse(localStorage.getItem(`conversation:${conversation_id}`));

	before_adding.items.push({
		role: role,
		content: content,
	});

	localStorage.setItem(`conversation:${conversation_id}`, JSON.stringify(before_adding)); // update conversation
};


const handleDownload = () => {
	// Fetch the chat history from the server and initiate the download
	fetch("/files_download")
		.then((response) => response.blob())
		.then((blob) => {
			// Create a URL for the blob
			const url = URL.createObjectURL(blob);
			// Create a link element and set its properties for the download
			const link = document.createElement("a");
			link.href = url;
			link.download = "ikyet.zip";
			// Simulate a click on the link to trigger the download
			link.click();
			// Clean up the URL object after the download
			URL.revokeObjectURL(url);
		})
		.catch((error) => {
			console.error("Error:", error);
		});
};
const load_conversations = async (limit, offset, loader) => {
	//console.log(loader);
	//if (loader === undefined) box_conversations.appendChild(spinner);

	let conversations = [];
	for (let i = 0; i < localStorage.length; i++) {
		if (localStorage.key(i).startsWith("conversation:")) {
			let conversation = localStorage.getItem(localStorage.key(i));
			conversations.push(JSON.parse(conversation));
		}
	}

	//if (loader === undefined) spinner.parentNode.removeChild(spinner)
	await clear_conversations();

	for (conversation of conversations) {
		box_conversations.innerHTML += `
            <div class="conversation-sidebar">
                <div class="left" onclick="set_conversation('${conversation.id}')">
                    <i class="fa-regular fa-comments"></i>
                    <span class="conversation-title">${conversation.title}</span>
                </div>
                <i onclick="delete_conversation('${conversation.id}')" class="fa-regular fa-trash"></i>
            </div>
        `;
	}

	document.querySelectorAll(`code`).forEach((el) => {
		hljs.highlightElement(el);
	});
};

document.getElementById(`cancelButton`).addEventListener(`click`, async () => {
	window.controller.abort();
	console.log(`aborted ${window.conversation_id}`);
});

function h2a(str1) {
	var hex = str1.toString();
	var str = "";

	for (var n = 0; n < hex.length; n += 2) {
		str += String.fromCharCode(parseInt(hex.substr(n, 2), 16));
	}

	return str;
}

const load_settings_localstorage = async () => {
	settings_ids = ["switch"];
	settings_elements = settings_ids.map((id) => document.getElementById(id));
	settings_elements.map((element) => {
		if (localStorage.getItem(element.id)) {
			switch (element.type) {
				case "checkbox":
					element.checked = localStorage.getItem(element.id) === "true";
					break;
				case "select-one":
					element.selectedIndex = parseInt(localStorage.getItem(element.id));
					break;
				default:
					console.warn("Unresolved element type");
			}
		}
	});
};
const uuid = () => {
	return `xxxxxxxx-xxxx-4xxx-yxxx-${Date.now().toString(16)}`.replace(/[xy]/g, function (c) {
		var r = (Math.random() * 16) | 0,
			v = c == "x" ? r : (r & 0x3) | 0x8;
		return v.toString(16);
	});
};

const message_id = () => {
	random_bytes = (Math.floor(Math.random() * 1338377565) + 2956589730).toString(2);
	unix = Math.floor(Date.now() / 1000).toString(2);

	return BigInt(`0b${unix}${random_bytes}`).toString();
};

window.onload = async () => {
	load_settings_localstorage();

	conversations = 0;
	for (let i = 0; i < localStorage.length; i++) {
		if (localStorage.key(i).startsWith("conversation:")) {
			conversations += 1;
		}
	}

	if (conversations == 0) localStorage.clear();

	await setTimeout(() => {
		load_conversations(20, 0);
	}, 1);

	if (!window.location.href.endsWith(`#`)) {
		if (/\/chat\/.+/.test(window.location.href.slice(url_prefix.length))) {
			await load_conversation(window.conversation_id);
		}
	}


	document.querySelector(".mobile-sidebar").addEventListener("click", (event) => {
		const sidebar = document.querySelector(".sidebar");

		if (sidebar.classList.contains("shown")) {
			sidebar.classList.remove("shown");
			event.target.classList.remove("rotated");
			document.body.style.overflow = "auto";
		} else {
			sidebar.classList.add("shown");
			event.target.classList.add("rotated");
			document.body.style.overflow = "hidden";
		}

		window.scrollTo(0, 0);
	});

	const register_settings_localstorage = async () => {
		settings_ids = ["switch"];
		settings_elements = settings_ids.map((id) => document.getElementById(id));
		settings_elements.map((element) =>
			element.addEventListener(`change`, async (event) => {
				switch (event.target.type) {
					case "checkbox":
						localStorage.setItem(event.target.id, event.target.checked);
						break;
					case "select-one":
						localStorage.setItem(event.target.id, event.target.selectedIndex);
						break;
					default:
						console.warn("Unresolved element type");
				}
			})
		);
	};

	message_input.addEventListener("keydown", async (evt) => {
		if (prompt_lock) return;
		if (evt.key === 13 && message_input.value.trim() !== "") {
			evt.preventDefault();
			await startResearch();
		}

		if (evt.key === "Enter" && !evt.shiftKey) {
			evt.preventDefault();
			await startResearch();
		}
	});

	send_button.addEventListener("click", async (event) => {
		event.preventDefault();
		if (prompt_lock) return;
		message_input.blur();
		await startResearch();
	});

	await register_settings_localstorage();
};


const gradients = [
	'linear-gradient( 135deg, #CE9FFC 10%, #7367F0 100%)',
	'linear-gradient( 135deg, #FFF6B7 10%, #F6416C 100%)',
	'linear-gradient( 135deg, #ABDCFF 10%, #0396FF 100%)',
	'linear-gradient( 135deg, #F97794 10%, #623AA2 100%)',
	'linear-gradient( 135deg, #F761A1 10%, #8C1BAB 100%)',
	'linear-gradient( 135deg, #5EFCE8 10%, #736EFE 100%)',
	'linear-gradient( 135deg, #52E5E7 10%, #130CB7 100%)',
	'linear-gradient( 135deg, #79F1A4 10%, #0E5CAD 100%)',
	'linear-gradient( 135deg, #2AFADF 10%, #4C83FF 100%)',
	'linear-gradient( 135deg, #F05F57 10%, #360940 100%)',
	'linear-gradient( 135deg, #97ABFF 10%, #123597 100%)',
	'linear-gradient( 135deg, #FF6FD8 10%, #3813C2 100%)',
	'linear-gradient( 135deg, #F0FF00 10%, #58CFFB 100%)',
	'linear-gradient( 135deg, #69FF97 10%, #00E4FF 100%)',
	'linear-gradient( 135deg, #F6D242 10%, #FF52E5 100%)',
	'linear-gradient( 135deg, #FAB2FF 10%, #1904E5 100%)',
	'linear-gradient( 135deg, #3C8CE7 10%, #00EAFF 100%)',
	'linear-gradient( 135deg, #FFA8A8 10%, #FCFF00 100%)',
	'linear-gradient( 135deg, #FF96F9 10%, #C32BAC 100%)',
	'linear-gradient( 135deg, #FFF720 10%, #3CD500 100%)',
	'linear-gradient( 135deg, #FFF886 10%, #F072B6 100%)',
	'linear-gradient(45deg, #85FFBD 0%, #FFFB7D 100%)',
	'linear-gradient(135deg, #65FDF0 10%, #1D6FA3 100%)',
	'linear-gradient(135deg, #FF7AF5 10%, #513162 100%)',
	'linear-gradient(135deg, #3B2667 10%, #BC78EC 100%)',
	'linear-gradient(25deg, #e76830, #e6994b, #dec667, #cef184)',
	'linear-gradient(25deg, #18005a, #5b2888, #9a55b9, #dc84ec)',
	'linear-gradient(25deg, #2fdbb9, #97dd95, #cdde6e, #f8de3e)',
	'linear-gradient(25deg, #100e20, #2b504f, #439a84, #57ecbc)',
	'linear-gradient(25deg, #c4a2f0, #d7b8de, #e6cfca, #f3e6b6)',
	'linear-gradient(25deg, #002a46, #166173, #299ea4, #3adfd7)',
	'linear-gradient(45deg, #dacb93, #a7b58a, #719f82, #2b8979)',
	'linear-gradient(320deg, #340e5f, #641a6a, #922976, #bf3981)',
	'linear-gradient(45deg, #2f2352, #6d365a, #a74c61, #e26267)',
	'linear-gradient(25deg, #222229, #343b5a, #44568f, #5172c9)',
	'linear-gradient(25deg, #4ad3a2, #9fd482, #d3d55f, #ffd432)',
	'linear-gradient(25deg, #1a3f48, #2b6f6e, #3ba396, #4bdbc0)',
	'linear-gradient(25deg, #15f8e8, #a4edb5, #d9e282, #ffd647)',
	'linear-gradient(25deg, #274042, #3e6a64, #569789, #6fc6af)',
	'linear-gradient(25deg, #1b182d, #345b5b, #43a78c, #49fac0)',
	'linear-gradient(25deg, #d3814b, #e5a376, #f3c5a3, #ffe8d1)',
	'linear-gradient(25deg, #de225c, #e7727d, #ebaa9f, #e6dfc4)',
	'linear-gradient(25deg, #ca557e, #de8899, #f0b8b5, #ffe8d1)',
	'linear-gradient(25deg, #271e56, #683360, #a44b68, #e06570)',
	'linear-gradient(25deg, #2c2a5e, #385881, #3b89a6, #33bccc)',
	'linear-gradient(25deg, #066289, #1390a9, #15c0ca, #08f3ec)'
];

// Generate a random index to select a gradient
function generateRandomIndex() {
	return Math.floor(Math.random() * gradients.length);
}

// Set the random gradient as the background
function setRandomBackground() {
	const index = generateRandomIndex();
	const gradient = gradients[index];
	document.body.style.backgroundImage = gradient;
}

/*
function clearTextarea(textarea) {
	textarea.style.removeProperty("height");
	textarea.style.height = `${textarea.scrollHeight + 4}px`;

	if (textarea.value.trim() === "" && textarea.value.includes("\n")) {
		textarea.value = "";
	}
}
*/

download_button.addEventListener("click", handleDownload);
window.addEventListener('load', setRandomBackground);
/*document.getElementById("fileForm").addEventListener("submit", function (event) {
	event.preventDefault(); // Prevent form submission and page refresh
	processFile();
});

 */

