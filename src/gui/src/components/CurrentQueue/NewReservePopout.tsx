import React from "react"
import { useForm } from "antd/lib/form/Form";
import { Button, Input, Form, Modal } from "antd";
import { IBallChaser } from "../../types";

interface INewReservePopout {
  open: boolean;
  onClose: () => void;
  onNewReserve: (newReserve: IBallChaser) => void;
}

export default function NewReservePopout(props: INewReservePopout) {  
  const [newReserveForm] = useForm();

  return (
    <Modal
      title="Add Reserve"
      visible={props.open}
      onCancel={() => {props.onClose(); newReserveForm.resetFields()}}
      footer={[
        <Button key="cancel" onClick={() => {props.onClose(); newReserveForm.resetFields()}}>
          Cancel
        </Button>,
        <Button key="newReserveSubmitBtn" form="newReserveForm" type="primary" htmlType="submit">
          Add Reserve
        </Button>,
      ]}
    >
      <Form
        form={newReserveForm}
        id="newReserveForm"
        layout="vertical"
        onFinish={(values) => {props.onNewReserve(values as IBallChaser); newReserveForm.resetFields()}}
      >
        <Form.Item
          label="Player ID"
          name="id"
          rules={[{
            required: true,
            type: "string",
            min: 15,
            max: 20,
          }]}
        >
          <Input/>
        </Form.Item>
        <Form.Item
          label="Player Name"
          name="name"
          rules={[{
            required: true,
            type: "string",
            min: 6,
          }]}
        >
          <Input/>
        </Form.Item>
      </Form>
    </Modal>
  )
}