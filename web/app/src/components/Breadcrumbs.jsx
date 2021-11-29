import Breadcrumb from "react-bootstrap/Breadcrumb";

export default function Breadcrumbs(props) {
  return (
    <Breadcrumb>
      {props.level?.map
        ? props.level.map((_level, idx) => {
            return (
              <Breadcrumb.Item
                key={idx}
                onClick={() => props.click(idx, _level)}
                href=""
              >
                {_level}
              </Breadcrumb.Item>
            );
          })
        : ""}
    </Breadcrumb>
  );
}
