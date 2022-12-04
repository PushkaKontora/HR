import {useState} from 'react';
import {TabParent, Tab} from './styled';

type FavoriteTabManagerProps = {
  tabNames: readonly string[],
  clickHandler?: (tabIndex: number) => void
};

export function FavoriteTabManager(props: FavoriteTabManagerProps) {
  const [selectedTab, setSelectedTab] = useState(0);

  const click = (index: number) => {
    if (props.clickHandler)
      props.clickHandler(index);

    setSelectedTab(index);
  };

  return (
    <TabParent as={'section'}>
      {
        props.tabNames.map((item, idx) => {
          return (
            <Tab selected={selectedTab === idx} key={idx} onClick={() => {click(idx);}}>
              {item}
            </Tab>);
        })
      }
    </TabParent>
  );
}
