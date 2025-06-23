#define MINIAUDIO_IMPLEMENTATION

#include "miniaudio.h"
#include <stdio.h>
#include <string.h>
#include <pthread.h>

// Definisi global untuk variabel yang sebelumnya hanya dideklarasikan
int paused = 0;
int stopped = 0;
pthread_mutex_t pause_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t pause_cond = PTHREAD_COND_INITIALIZER;

typedef struct {
  FILE* stream;
} playback_context;

void data_callback(ma_device* pDevice, void* pOutput, const void* pInput, ma_uint32 frameCount) {
  playback_context* ctx = (playback_context*)pDevice->pUserData;

  pthread_mutex_lock(&pause_mutex);
  while (paused && !stopped) {
    pthread_cond_wait(&pause_cond, &pause_mutex);
  }
  pthread_mutex_unlock(&pause_mutex);

  size_t bytesPerFrame = ma_get_bytes_per_frame(ma_format_s16, 1);
  size_t bytesToRead = frameCount * bytesPerFrame;
  size_t bytesRead = fread(pOutput, 1, bytesToRead, ctx->stream);

  // Jika kurang dari yang diminta, sisanya di-isi 0 (silence)
  if (bytesRead < bytesToRead) {
    memset((char*)pOutput + bytesRead, 0, bytesToRead - bytesRead);
  }
}

void play_stream(FILE* stream) {
  playback_context ctx = { .stream = stream };

  ma_device_config config = ma_device_config_init(ma_device_type_playback);
  config.playback.format = ma_format_s16;
  config.playback.channels = 1;
  config.sampleRate = 22050;
  config.dataCallback = data_callback;
  config.pUserData = &ctx;

  ma_device device;
  if (ma_device_init(NULL, &config, &device) != MA_SUCCESS) {
    fprintf(stderr, "Failed to init device.\n");
    return;
  }

  if (ma_device_start(&device) != MA_SUCCESS) {
    fprintf(stderr, "Failed to start device.\n");
    ma_device_uninit(&device);
    return;
  }

  // Tunggu sampai stream selesai
  while (!stopped && !feof(stream)) {
    ma_sleep(100);
  }

  ma_device_uninit(&device);
  fclose(stream);
}

void audio_pause() {
  pthread_mutex_lock(&pause_mutex);
  paused = 1;
  pthread_mutex_unlock(&pause_mutex);
}

void audio_resume() {
  pthread_mutex_lock(&pause_mutex);
  paused = 0;
  pthread_cond_signal(&pause_cond);  // Bangunkan thread audio
  pthread_mutex_unlock(&pause_mutex);
}

void audio_stop() {
  pthread_mutex_lock(&pause_mutex);
  stopped = 1;
  pthread_cond_signal(&pause_cond);  // Wake in case it's paused
  pthread_mutex_unlock(&pause_mutex);
}

void play_stream_fd(int fd) {
  FILE* stream = fdopen(fd, "r");
  if (stream != NULL) {
    play_stream(stream);
  } else {
    fprintf(stderr, "fdopen() failed\n");
  }
}