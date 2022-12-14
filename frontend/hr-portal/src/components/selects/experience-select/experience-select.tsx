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
  onChange?: (e: {value: string, label: string}) => void,
  width?: string
}

export function ExperienceSelect({name, selectedValue, controllerValue, onChange, width}: ExperienceSelectProps) {
  return (
    <ProfileSelect onChange={onChange} controllerValue={controllerValue} name={name} options={OPTIONS} placeholder={'Не выбран'}
      value={OPTIONS.find((item) => selectedValue === item.value)}
      width={width}/>
  );
}
