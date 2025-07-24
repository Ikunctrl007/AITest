<template>
  <el-card class="chat-container" shadow="hover">
    <el-scrollbar
      ref="scrollbar"
      class="chat-box"
      style="height: 500px; overflow-y: auto"
      :noresize="false"
    >
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['chat-message', msg.role === 'user' ? 'user' : 'assistant']"
      >
        <el-avatar
          :size="30"
          :icon="
            msg.role === 'user' ? 'el-icon-user' : 'el-icon-chat-line-round'
          "
          class="avatar"
        ></el-avatar>
        <div class="message-content">
          <div class="role-name">
            {{ msg.role === "user" ? "你" : "通义千问" }}：
          </div>
          <div class="content">{{ msg.content }}</div>
        </div>
      </div>
    </el-scrollbar>

    <el-input
      v-model="userInput"
      placeholder="请输入你的问题..."
      @keyup.enter.native="sendMessage"
      clearable
      class="input-area"
      :maxlength="500"
      show-word-limit
      :disabled="loading"
    >
      <template #append>
        <el-button
          type="primary"
          @click="sendMessage"
          :loading="loading"
          :disabled="loading"
        >
          发送
        </el-button>
      </template>
    </el-input>
  </el-card>
</template>

<script setup>
import { ref, nextTick } from "vue";
import axios from "axios";

const userInput = ref("");
const messages = ref([]);
const loading = ref(false);

const scrollbar = ref(null);

const sendMessage = async () => {
  const content = userInput.value.trim();
  if (!content || loading.value) return; // 防止重复发送

  loading.value = true;

  messages.value.push({ role: "user", content });
  userInput.value = "";

  await nextTick();
  if (scrollbar.value && scrollbar.value.wrap) {
    scrollbar.value.wrap.scrollTop = scrollbar.value.wrap.scrollHeight;
  }

  try {
    const res = await axios.post("http://localhost:8000/chat", {
      message: content,
    });
    const reply = res.data.reply || res.data.error || "AI 没有回复";
    messages.value.push({ role: "assistant", content: reply });
  } catch (error) {
    messages.value.push({
      role: "assistant",
      content: "请求出错，请检查网络或服务状态",
    });
  }

  await nextTick();
  if (scrollbar.value && scrollbar.value.wrap) {
    scrollbar.value.wrap.scrollTop = scrollbar.value.wrap.scrollHeight;
  }

  loading.value = false;
};
</script>

<style scoped>
.chat-container {
  max-width: 700px;
  margin: 50px auto;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  padding: 20px;
}

.chat-box {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
}

.chat-message {
  display: flex;
  align-items: flex-start;
  margin: 10px 0;
}

.user {
  flex-direction: row-reverse;
  text-align: right;
}

.user .message-content {
  background-color: #409eff;
  color: white;
  border-radius: 15px 15px 0 15px;
  padding: 10px 15px;
  max-width: 70%;
}

.assistant .message-content {
  background-color: #e6e6e6;
  color: #333;
  border-radius: 15px 15px 15px 0;
  padding: 10px 15px;
  max-width: 70%;
}

.avatar {
  margin: 0 10px;
  color: #409eff;
}

.role-name {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 14px;
}

.content {
  white-space: pre-wrap;
  word-break: break-word;
}
.input-area {
  width: 100%;
}
</style>
