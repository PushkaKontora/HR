import {TIMES_RU} from '../const/time-names';
import {NAMES_FOUND_ENDINGS, NAMES_VACANCIES_ENDINGS} from '../const';

function getAppropriateTimeName(names: string[], time: number) {
  const lastTwo = time % 100;
  if (lastTwo >= 10 && lastTwo <= 19)
    return names[2];

  const last = lastTwo % 10;
  if (last >= 5 && last <= 9 || last == 0)
    return names[2];
  else if (last >= 2 && last <= 4)
    return names[1];

  return names[0];
}

export function getBackTimestampRussian(date: Date | null | undefined) {
  if (!date)
    return undefined;

  let diff = Date.now() - (new Date(date)).getTime();
  let num = diff;
  let timeName = TIMES_RU.recently;

  if (diff >= 60 * 1000) {
    diff = Math.floor(diff / 1000 / 60); // минуты
    if (diff >= 60) {
      diff = Math.floor(diff / 60); // часы
      if (diff >= 24) {
        diff = Math.floor(diff / 24); // дни
        if (diff >= 7) {
          const days = diff;
          diff = Math.floor(diff / 7); // недели
          if (days >= 30) {
            diff = Math.floor(days / 30); // месяцы
            if (diff >= 12) {
              num = Math.floor(diff / 12); // года
              timeName = getAppropriateTimeName(TIMES_RU.years, diff);
            } else {
              num = diff;
              timeName = getAppropriateTimeName(TIMES_RU.months, diff);
            }
          } else {
            num = diff;
            timeName = getAppropriateTimeName(TIMES_RU.weeks, diff);
          }
        } else {
          num = diff;
          timeName = getAppropriateTimeName(TIMES_RU.days, diff);
        }
      } else {
        num = diff;
        timeName = getAppropriateTimeName(TIMES_RU.hours, diff);
      }
    } else {
      num = diff;
      timeName = getAppropriateTimeName(TIMES_RU.minutes, diff);
    }
  }

  if (timeName === TIMES_RU.recently) {
    return `${TIMES_RU.recently}`;
  }
  return `${num} ${timeName} ${TIMES_RU.back}`;
}

export function getCorrectEndingsInVacancies(countVacancies: number): string {
  const lineResult = [getAppropriateTimeName(NAMES_FOUND_ENDINGS, countVacancies), countVacancies, getAppropriateTimeName(NAMES_VACANCIES_ENDINGS, countVacancies)].join(' ');
  return lineResult;
}