import React from "react";
import { eel } from "../../App";
import { IConfig } from "../../types";
import { Card, Form, Input, Switch, Button, Spin, Typography } from "antd";
import "./ConfigOptions.scss";

const PlainTextSwitch = React.forwardRef((props: {handleChange: () => void}, ref) => (
  <>
    <Typography.Text className="switchLabel">Show as plain text</Typography.Text>
    <Switch defaultChecked={false} onChange={props.handleChange} ref={ref as any} />
  </>
));

export default function ConfigOptions() {
  const [config, setConfig] = React.useState<IConfig>();
  const [showPlainText, setShowPlainText] = React.useState<boolean>(false);

  React.useEffect(() => {
    eel.getConfig()((configSettings: IConfig) => setConfig(configSettings))
  }, []);

  if (!config) {
    return (
      <Card title="Config Options" className="configForm">
        <Spin/>
      </Card>
    )
  }

  return (
    <Card 
      title="Config Options"
      extra={<PlainTextSwitch handleChange={() => setShowPlainText(!showPlainText)}/>} 
      className="configForm"
    >
      <Form layout="vertical" initialValues={config}>
        <Form.Item
          label="AWS ID"
          name="aws_access_key_id"
          required
        >
          <Input type={showPlainText ? "text" : "password"} />
        </Form.Item>
        <Form.Item
          label="AWS Secret Key"
          name="aws_secret_access_key"
          required
        >
          <Input type={showPlainText ? "text" : "password"} />
        </Form.Item>
        <Form.Item
          label="Discord Bot Token"
          name="token"
          required
        >
          <Input type={showPlainText ? "text" : "password"} />
        </Form.Item>
        <Form.Item>
          <Button size="large" type="primary" htmlType="submit" className="submitBtn">
            Save Changes
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}