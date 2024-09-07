import { StyleSheet, Text, TouchableOpacity } from "react-native";
import { Modal, View } from "react-native";
import { SvgXml } from "react-native-svg";
import { closeIcon, warningIcon } from "../images/images";
import { useState } from "react";

const ModalDeteleAccount = () => {
  const [modalVisible, setModalVisible] = useState(false);
  return (
    <View>
      <TouchableOpacity onPress={() => setModalVisible(true)}>
        <Text style={styles.actionButtonText}>Удалить аккаунт</Text>
      </TouchableOpacity>
      {modalVisible && (
        <Modal
          animationType="fade"
          transparent={true}
          visible={modalVisible}
          onRequestClose={() => {
            setModalVisible(!modalVisible);
          }}
        >
          <View style={styles.centeredView}>
            <TouchableOpacity
              style={styles.closeButton}
              onPress={() => setModalVisible(!modalVisible)}
            >
              <SvgXml xml={closeIcon} />
            </TouchableOpacity>
            <View style={styles.modalView}>
              <SvgXml xml={warningIcon} />

              <Text style={styles.warningText}>
                Вы действительно хотите удалить аккаунт?
              </Text>
              <View style={styles.buttons}>
                <TouchableOpacity
                  style={[styles.button, styles.buttonClose]}
                  onPress={() => setModalVisible(!modalVisible)}
                >
                  <Text style={styles.buttonCloseText}>Нет</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.button, styles.buttonDelete]}
                  onPress={() => setModalVisible(!modalVisible)}
                >
                  <Text style={styles.buttonDeleteText}>Да</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  actionButtons: {
    alignItems: "center",
    marginTop: 30,
    gap: 15,
    marginBottom: 100,
  },
  actionButtonText: {
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
  centeredView: {
    position: "relative",
    width: "100%",
    height: "100%",
    backgroundColor: "rgba(52, 52, 52, 0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalView: {
    marginHorizontal: 38,
    backgroundColor: "white",
    borderRadius: 30,
    paddingVertical: 40,
    paddingHorizontal: 30,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  warningText: {
    marginTop: 20,
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMSemiBold",
    fontSize: 18,
    textAlign: "center",
  },
  buttons: {
    marginTop: 20,
    gap: 15,
  },
  button: {
    justifyContent: "center",
    alignItems: "center",
    minWidth: "100%",
    paddingHorizontal: 20,
    borderRadius: 10,
    height: 40,
  },
  buttonDelete: {
    borderWidth: 1,
    borderEndColor: "rgba(22, 3, 111, 1)",
  },
  buttonClose: {
    backgroundColor: "rgba(48, 31, 129, 1)",
  },
  buttonCloseText: {
    color: "white",
    fontFamily: "IBMSemiBold",
  },
  buttonDeleteText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMMedium",
  },
  closeButton: {
    position: "absolute",
    top: "25%",
    right: "7%",
  },
});

export default ModalDeteleAccount;
