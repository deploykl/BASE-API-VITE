<template>
  <div class="clock">
    <p>{{ time }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      time: this.getCurrentTime(),
      timer: null,
    };
  },
  methods: {
    getCurrentTime() {
      const now = new Date();
      // Formatea la hora en formato 12 horas con AM/PM
      const time = now.toLocaleTimeString('es-PE', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
      });

      // Formatea la fecha en el formato "10 de ago."
      const options = { day: 'numeric', month: 'short' };
      const date = now.toLocaleDateString('es-PE', options).replace('.', ''); // Quita el punto del mes

      return `${date},  ${time}`;
    },
    updateClock() {
      this.time = this.getCurrentTime();
    },
  },
  mounted() {
    // Actualiza el reloj cada segundo
    this.timer = setInterval(this.updateClock, 1000);
  },
  beforeDestroy() {
    // Limpia el intervalo cuando el componente se destruye
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
.clock {
  text-align: center;
  font-family: Arial, sans-serif;
  font-size: 1.1rem;
  margin-top: 16px;
  color: gray;
}
</style>

