export function extractFileNameFromYandex(storageName: string | undefined) {
  if (!storageName) {
    return undefined;
  }

  return decodeURI(storageName.split('?')[0].split('/').reverse()[0].split('_')[1]);
}
