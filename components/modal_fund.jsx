import { useNavigation } from "@react-navigation/native";
import {
  Modal,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import GestureRecognizer from "react-native-swipe-gestures";
import CheckBox from "react-native-check-box";
import { useState } from "react";
import { SvgXml } from "react-native-svg";

import { minusIcon, plusIcon } from "../images/images";

const ModalFund = ({ width = "" }) => {
  const navigation = useNavigation();

  const [data, setData] = useState({
    modalVisible: false,
    selectPeriod: [1, 0, 0],
    selectTypeSum: [0, 0, 0, 0, 0, 0],
    checkButton: false,
    sum: 10,
  });

  let copiedData = { ...data };

  return (
    <View>
      <TouchableOpacity
        style={[styles.button, styles.helpButton, { minWidth: `${width}` }]}
        onPress={() => {
          copiedData.modalVisible = true;
          setData(copiedData);
        }}
      >
        <Text style={styles.helpText}>Помочь</Text>
      </TouchableOpacity>
      {copiedData.modalVisible && (
        <GestureRecognizer
          style={{ flex: 1 }}
          onSwipeUp={() => {
            copiedData.modalVisible = true;
            setData(copiedData);
          }}
          onSwipeDown={() => {
            copiedData.modalVisible = false;
            setData(copiedData);
          }}
        >
          <Modal
            animationType="slide"
            visible={copiedData.modalVisible}
            presentationStyle="formSheet"
          >
            <View style={styles.swipeLine} />
            <ScrollView automaticallyAdjustKeyboardInsets={true}>
              <Text style={styles.modalHeaderText}>
                Ремонт дома для пожилой пары
              </Text>
              <View style={styles.modalInfo}>
                <View style={[styles.component, styles.periodSelect]}>
                  <View style={styles.periodRow}>
                    <TouchableOpacity
                      onPress={() => {
                        copiedData.selectPeriod = [1, 0, 0];
                        setData(copiedData);
                      }}
                      style={[
                        styles.periodButton,
                        data.selectPeriod[0] == 1
                          ? styles.activePeriodButton
                          : null,
                      ]}
                    >
                      <Text
                        style={[
                          styles.periodButtonText,
                          data.selectPeriod[0] == 1
                            ? styles.activePeroidButtonText
                            : null,
                        ]}
                      >
                        Каждый день
                      </Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      onPress={() => {
                        copiedData.selectPeriod = [0, 1, 0];
                        setData(copiedData);
                      }}
                      style={[
                        styles.periodButton,
                        data.selectPeriod[1] == 1
                          ? styles.activePeriodButton
                          : null,
                      ]}
                    >
                      <Text
                        style={[
                          styles.periodButtonText,
                          data.selectPeriod[1] == 1
                            ? styles.activePeroidButtonText
                            : null,
                        ]}
                      >
                        Каждый месяц
                      </Text>
                    </TouchableOpacity>
                  </View>

                  <View style={styles.periodRow}>
                    <TouchableOpacity
                      onPress={() => {
                        copiedData.selectPeriod = [0, 0, 1];
                        setData(copiedData);
                      }}
                      style={[
                        styles.periodButton,
                        data.selectPeriod[2] == 1
                          ? styles.activePeriodButton
                          : null,
                      ]}
                    >
                      <Text
                        style={[
                          styles.periodButtonText,
                          data.selectPeriod[2] == 1
                            ? styles.activePeroidButtonText
                            : null,
                        ]}
                      >
                        Разовый платеж
                      </Text>
                    </TouchableOpacity>
                  </View>
                </View>
                <Text style={styles.selectSumHeaderText}>
                  Выберите для себя комфортную сумму
                </Text>
                <View style={styles.selectSum}>
                  <View style={styles.handledSumSelect}>
                    <TouchableOpacity
                      style={[styles.componentMoney, styles.minusSum]}
                      onPress={() => {
                        copiedData.selectTypeSum = [1, 0, 0, 0, 0, 0];
                        copiedData.sum == 10
                          ? (copiedData.sum = 10)
                          : (copiedData.sum = copiedData.sum - 10);
                        setData(copiedData);
                      }}
                    >
                      <SvgXml xml={minusIcon} />
                    </TouchableOpacity>
                    <View
                      style={[
                        styles.componentMoney,
                        styles.sumView,
                        data.selectTypeSum[0] == 1
                          ? styles.activeSumView
                          : null,
                      ]}
                    >
                      <Text style={styles.sumViewText}>
                        {data.sum} ₽
                        {data.selectPeriod[0] == 1
                          ? " в день"
                          : data.selectPeriod[1] == 1
                          ? " в месяц"
                          : null}
                      </Text>
                    </View>
                    <TouchableOpacity
                      style={[styles.componentMoney, styles.plusSum]}
                      onPress={() => {
                        copiedData.sum = copiedData.sum + 10;
                        setData(copiedData);
                      }}
                    >
                      <SvgXml xml={plusIcon} />
                    </TouchableOpacity>
                  </View>
                  <View style={styles.autoSumSelect}>
                    <TouchableOpacity
                      style={[
                        styles.componentMoney,
                        styles.autoSumButton,
                        data.selectTypeSum[1] == 1
                          ? styles.activeAutoSumButton
                          : null,
                      ]}
                      onPress={() => {
                        copiedData.selectTypeSum = [0, 1, 0, 0, 0, 0];
                        copiedData.sum = 200;
                        setData(copiedData);
                      }}
                    >
                      <Text
                        style={[
                          styles.autoSumButtonText,
                          data.selectTypeSum[1] == 1
                            ? styles.activeAutoSumButtonText
                            : null,
                        ]}
                      >
                        200 ₽
                      </Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[
                        styles.componentMoney,
                        styles.autoSumButton,
                        data.selectTypeSum[2] == 1
                          ? styles.activeAutoSumButton
                          : null,
                      ]}
                      onPress={() => {
                        copiedData.selectTypeSum = [0, 0, 1, 0, 0, 0];
                        copiedData.sum = 400;
                        setData(copiedData);
                      }}
                    >
                      <Text
                        style={[
                          styles.autoSumButtonText,
                          data.selectTypeSum[2] == 1
                            ? styles.activeAutoSumButtonText
                            : null,
                        ]}
                      >
                        400 ₽
                      </Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[
                        styles.componentMoney,
                        styles.autoSumButton,
                        data.selectTypeSum[3] == 1
                          ? styles.activeAutoSumButton
                          : null,
                      ]}
                      onPress={() => {
                        copiedData.selectTypeSum = [0, 0, 0, 1, 0, 0];
                        copiedData.sum = 900;
                        setData(copiedData);
                      }}
                    >
                      <Text
                        style={[
                          styles.autoSumButtonText,
                          data.selectTypeSum[3] == 1
                            ? styles.activeAutoSumButtonText
                            : null,
                        ]}
                      >
                        900 ₽
                      </Text>
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[
                        styles.componentMoney,
                        styles.autoSumButton,
                        data.selectTypeSum[4] == 1
                          ? styles.activeAutoSumButton
                          : null,
                      ]}
                      onPress={() => {
                        copiedData.selectTypeSum = [0, 0, 0, 0, 1, 0];
                        copiedData.sum = 1000;
                        setData(copiedData);
                      }}
                    >
                      <Text
                        style={[
                          styles.autoSumButtonText,
                          data.selectTypeSum[4] == 1
                            ? styles.activeAutoSumButtonText
                            : null,
                        ]}
                      >
                        1000 ₽
                      </Text>
                    </TouchableOpacity>
                  </View>
                  <View
                    style={[
                      styles.inputSelect,
                      data.selectTypeSum[5] == 1
                        ? styles.activeInputSelect
                        : null,
                    ]}
                  >
                    <View style={styles.componentMoney}>
                      <TextInput
                        onPress={() => {
                          copiedData.selectTypeSum = [0, 0, 0, 0, 0, 1];
                          setData(copiedData);
                        }}
                        placeholder="Ваша сумма"
                        placeholderTextColor="rgba(183, 183, 183, 1)"
                        keyboardType="number-pad"
                        style={styles.inputSum}
                        onChange={(textInput) => {
                          copiedData.sum = textInput.nativeEvent.text;
                          setData(copiedData);
                        }}
                      />
                    </View>
                  </View>
                  <View style={[styles.component]}>
                    <Text style={styles.payInfoHeaderText}>
                      Информация о платеже
                    </Text>
                    <View style={styles.payInfo}>
                      <View style={styles.divideLine} />
                      <View style={styles.payInfoRow}>
                        <Text style={styles.payInfoAtrribute}>
                          Сумма платежа
                        </Text>
                        <Text style={styles.payInfoValue}>{data.sum} ₽</Text>
                      </View>
                      <View style={styles.divideLine} />
                      <View style={styles.payInfoRow}>
                        <Text style={styles.payInfoAtrribute}>Вид платежа</Text>
                        <Text style={styles.payInfoValue}>
                          {data.selectPeriod[0] == 1
                            ? "Каждый день"
                            : data.selectPeriod[1] == 1
                            ? "Каждый месяц"
                            : data.selectPeriod[2] == 1
                            ? "Разовый платеж"
                            : ""}
                        </Text>
                      </View>
                    </View>
                    <TouchableOpacity style={styles.payButton}>
                      <Text style={styles.payButtonText}>Оплатить</Text>
                    </TouchableOpacity>

                    <View style={styles.agreeView}>
                      <CheckBox
                        isChecked={copiedData.checkButton}
                        onClick={() => {
                          copiedData.checkButton = !copiedData.checkButton;
                          setData(copiedData);
                        }}
                      />
                      <Text style={styles.agreeText}>
                        Согласен с условиями Пользовательского соглашения
                        и Политики обработки персональных данных
                      </Text>
                    </View>
                  </View>
                </View>
              </View>
            </ScrollView>
          </Modal>
        </GestureRecognizer>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  button: {
    alignItems: "center",
    justifyContent: "center",
    height: 35,
    borderRadius: 10,
  },
  helpButton: {
    backgroundColor: "rgba(48, 31, 129, 1)",
  },
  helpText: {
    fontFamily: "IBMSemiBold",
    color: "white",
  },
  swipeLine: {
    width: "30%",
    height: 7,
    backgroundColor: "rgba(183, 183, 183, 1)",
    borderRadius: 5,
    alignSelf: "center",
    marginTop: 10,
  },
  modalHeaderText: {
    alignSelf: "center",
    marginTop: 40,
    paddingHorizontal: 86,
    fontSize: 22,
    fontFamily: "IBMSemiBold",
    color: "rgba(22, 3, 111, 1)",
    textAlign: "center",
  },

  component: {
    padding: 20,
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
  },
  modalInfo: {
    paddingHorizontal: 20,
    marginTop: 20,
    marginBottom: 20,
  },
  periodRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: 5,
  },
  periodButton: {
    justifyContent: "center",
    alignItems: "center",
    height: 30,
    backgroundColor: "rgba(237, 236, 240, 1)",
    flex: 1,
    borderRadius: 5,
  },
  activePeriodButton: {
    borderWidth: 1,
    borderColor: "rgba(22, 3, 111, 1)",
  },
  periodSelect: {
    gap: 5,
  },
  periodButtonText: {
    color: "rgba(52, 52, 52, 1)",
    fontSize: 12,
    fontFamily: "IBMMedium",
  },
  activePeroidButtonText: {
    color: "rgba(22, 3, 111, 1)",
  },
  selectSumHeaderText: {
    fontFamily: "IBMRegular",
    color: "rgba(52, 52, 52, 1)",
    alignSelf: "center",
    marginTop: 15,
  },

  componentMoney: {
    height: 50,
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 10,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
    justifyContent: "center",
    alignItems: "center",
  },
  minusSum: {
    width: 50,
  },
  plusSum: { width: 50 },

  selectSum: {
    marginTop: 15,
    gap: 15,
  },
  handledSumSelect: {
    flexDirection: "row",
    gap: 15,
  },
  sumView: {
    flex: 1,
  },
  sumViewText: {
    fontFamily: "IBMMedium",
    color: "rgba(22, 3, 111, 1)",
  },
  autoSumSelect: {
    flexDirection: "row",
    gap: 15,
  },
  autoSumButton: {
    flex: 1,
  },
  autoSumButtonText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
  },
  activeSumView: {
    borderWidth: 2,
    borderColor: "rgba(22, 3, 111, 1)",
  },
  activeAutoSumButton: {
    backgroundColor: "rgba(48, 31, 129, 1)",
  },
  activeAutoSumButtonText: {
    color: "white",
  },
  inputSum: {
    width: "100%",
    height: "100%",
    paddingHorizontal: 20,
  },
  activeInputSelect: {
    borderWidth: 2,
    borderColor: "rgba(22, 3, 111, 1)",
    borderRadius: 10,
  },
  divideLine: {
    width: "100%",
    height: 1,
    backgroundColor: "rgba(237, 236, 240, 1)",
  },
  payInfo: {
    marginTop: 15,
    gap: 10,
  },
  payInfoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  payInfoHeaderText: {
    fontFamily: "IBMMedium",
    color: "rgba(113, 113, 113, 1)",
  },
  payInfoAtrribute: {
    color: "rgba(183, 183, 183, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
  },
  payInfoValue: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
    fontSize: 12,
  },
  payButton: {
    alignItems: "center",
    marginTop: 15,
    height: 35,
    justifyContent: "center",
    backgroundColor: "rgba(48, 31, 129, 1)",
    borderRadius: 10,
  },
  payButtonText: {
    color: "white",
    fontFamily: "IBMSemiBold",
  },
  agreeView: {
    flexDirection: "row",
    marginTop: 15,
    gap: 8,
    alignItems: "center",
  },
  agreeText: {
    fontSize: 10,
    color: "rgba(183, 183, 183, 1)",
    fontFamily: "IBMMedium",
    paddingRight: 20,
  },
});

export default ModalFund;
