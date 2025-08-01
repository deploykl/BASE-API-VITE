<template>
  <div class="connection-manager">
    <slot
      :isOnline="isOnline"
      :isApiConnected="isApiConnected"
      :isCheckingApi="isCheckingApi"
      :lastApiCheck="lastApiCheck"
      :lastNetworkChange="lastNetworkChange"
      :checkApiConnection="checkApiConnection"
      :checkNetworkConnection="checkRealNetworkStatus"
    />
  </div>
</template>

<script setup>
import { useConnection } from './useConnection'

const {
  isOnline,
  isApiConnected,
  isCheckingApi,
  lastApiCheck,
  lastNetworkChange,
  checkApiConnection,
  checkRealNetworkStatus
} = useConnection()
</script>