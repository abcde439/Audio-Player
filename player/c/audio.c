#define MINIAUDIO_IMPLEMENTATION
#include "miniaudio.h"

ma_engine engine;
ma_sound sound;
int is_initialized = 0;

int start_audio(const char* path) {
  if (ma_engine_init(NULL, &engine) != MA_SUCCESS) {
		return -1;
  }

  if (ma_sound_init_from_file(&engine, path, MA_SOUND_FLAG_STREAM, NULL, NULL, &sound) != MA_SUCCESS) {
		ma_engine_uninit(&engine);
    return -2;
  }

  ma_sound_start(&sound);
  is_initialized = 1;
  return 0;
}

void pause_audio() {
  if (is_initialized) {
		ma_sound_stop(&sound);
  }
}

void resume_audio() {
  if (is_initialized) {
		ma_sound_start(&sound);
  }
}

void stop_audio() {
  if (is_initialized) {
    ma_sound_uninit(&sound);
    ma_engine_uninit(&engine);
    is_initialized = 0;
  }
}
