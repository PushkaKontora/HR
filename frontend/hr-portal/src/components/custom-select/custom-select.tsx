import Select from 'react-select';

import 'src/styles/custom-select.scss';

type CustomSelectProps = {
  options: any,
  onHandlerAction: () => void,
  name: string,
  placeholder: string
}

function CustomSelect({options, onHandlerAction, name, placeholder}: CustomSelectProps) {
  return (
    <Select
      className="basic-single"
      classNamePrefix="select"
      name={name}
      options={options}
      onChange={onHandlerAction}
      placeholder={placeholder}
    />
  );
}

export default CustomSelect;