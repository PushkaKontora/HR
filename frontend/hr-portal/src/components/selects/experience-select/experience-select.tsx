import {OptionType, ProfileSelect} from '../profile-select/profile-select';
import {ExperienceOptions} from '../../../types/experience-options';

export const OPTIONS: OptionType =
  (Object.keys(ExperienceOptions) as (keyof typeof ExperienceOptions)[])
    .map((item) => {
      return {
        'value': item,
        'label': ExperienceOptions[item]
      };
    });

export type ExperienceSelectProps = {
  name: string,
  selectedValue: string | undefined,
  controllerValue: string,
  onChange?: (e: {value: string, label: string}) => void
}

export function ExperienceSelect({name, selectedValue, controllerValue, onChange}: ExperienceSelectProps) {
  return (
    <ProfileSelect onChange={onChange} controllerValue={controllerValue} name={name} options={OPTIONS} placeholder={'Без опыта'}
      value={OPTIONS.find((item) => selectedValue === item.value)}/>
  );
}
