import CustomSelect from '../../custom-select/custom-select';
import {LargeLight} from '../../styled/fonts/large';
import Select from 'react-select';

export type OptionType = Array<{value: string, label: string}>;

export type ProfileSelectProps = {
  name: string,
  placeholder: string,
  options: OptionType,
  onChange?: (e: any) => void,
  value?: any,
  selectedOptions?: string[],
  controllerValue?: string,
  width?: string
}

export function ProfileSelect({name, placeholder, options, onChange, value, selectedOptions, controllerValue, width}: ProfileSelectProps) {
  const styles = {
    border: '0.5px solid black',
    borderRadius: '10px',
    color: 'black',
    padding: '4px 8px',
    width: width || 'auto'
  };

  return (
    <LargeLight>
      <CustomSelect
        controllerValue={controllerValue}
        value={value}
        styles={styles}
        options={options}
        onHandlerAction={onChange}
        name={name}
        placeholder={placeholder}
        selectedOptions={selectedOptions}/>
    </LargeLight>
  );
}