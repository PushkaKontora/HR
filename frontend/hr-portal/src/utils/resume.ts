import {ExperienceOptions} from '../types/experience-options';

export function extractFileNameFromYandex(storageName: string | undefined) {
  if (!storageName) {
    return undefined;
  }

  return decodeURI(storageName.split('?')[0].split('/').reverse()[0].split('_')[1]);
}

export function getExperienceOptionByKey(key: string) {
  return ExperienceOptions[key as keyof typeof ExperienceOptions];
}
