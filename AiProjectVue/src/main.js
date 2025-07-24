import { createApp } from "vue";
import App from "./App.vue";
import Chat from "./components/Chat.vue";

// 引入 Element Plus 样式和组件
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";

const app = createApp(App);

// 全局注册 Element Plus
app.use(ElementPlus);

// 全局注册聊天组件
app.component("Chat", Chat);

app.mount("#app");
