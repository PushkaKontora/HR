import Select from 'react-select';
import '../../styles/custom-select.scss';
import {ActionMeta, OnChangeValue} from 'react-select/dist/declarations/src/types';
import {OptionType} from '../selects/profile-select/profile-select';

type CustomSelectProps = {
  options: OptionType,
  onHandlerAction?: (e: any) => void,
  name: string,
  placeholder: string,
  styles?: any,
  value?: any,
  selectedOptions?: string[],
  controllerValue?: any
}

function CustomSelect({options, onHandlerAction, name, placeholder, styles, value, selectedOptions, controllerValue}: CustomSelectProps) {
  return (
    <Select
      className="basic-single"
      classNamePrefix="select"
      styles={{
        control: (baseStyles, state) => ({
          ...baseStyles,
          ...styles
        }),
      }}
      name={name}
      options={options}
      onChange={onHandlerAction}
      placeholder={placeholder}
      defaultValue={value}
      value={options.find((o) => o.value === controllerValue)}
      filterOption={(option) => !selectedOptions || !selectedOptions?.includes(option.value)}
    />
  );
}

export default CustomSelect;