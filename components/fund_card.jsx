import { useNavigation } from "@react-navigation/native";
import {
  Image,
  Modal,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from "react-native";
import GestureRecognizer from "react-native-swipe-gestures";
import { useState } from "react";
import { SvgXml } from "react-native-svg";
import { minusIcon, plusIcon } from "../images/images";

const FundCard = ({
  uri = "https://legacy.reactjs.org/logo-og.png",
  name = "Ремонт дома для пожилой пары",
  collect_sum = 30000,
  full_sum = 100000,
}) => {
  const [modalVisible, setModalVisible] = useState([1, 0, 0]);
  const navigation = useNavigation();
  const [isActive, setIsActive] = useState([0, 0, 0]);
  const [sum, setSum] = useState(30);
  const [selectTypeSum, setSelectTypeSum] = useState([0, 0, 0, 0, 0, 0]);
  return (
    <View style={styles.container}>
      <Image
        source={{ uri: uri }}
        height={150}
        width={"100%"}
        style={styles.mainImage}
      />

      <View style={styles.mainInfo}>
        <Text style={styles.nameText}>{name}</Text>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFillBar,
              { width: `${(collect_sum / full_sum) * 100}%` },
            ]}
          />
        </View>
        <View style={styles.progressSum}>
          <Text style={styles.moneyText}>
            {collect_sum.toLocaleString("ru")} ₽
          </Text>
          <Text style={styles.moneyText}>
            {full_sum.toLocaleString("ru")} ₽
          </Text>
        </View>
        <View style={styles.buttonsView}>
          <TouchableOpacity
            style={[styles.button, styles.detailsButton]}
            onPress={() => navigation.navigate("AboutFundScreen")}
          >
            <Text style={styles.detailsText}>Подробнее</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, styles.helpButton]}
            onPress={() => setModalVisible(true)}
          >
            <Text style={styles.helpText}>Помочь</Text>
          </TouchableOpacity>
        </View>
      </View>
      <GestureRecognizer
        style={{ flex: 1 }}
        onSwipeUp={() => setModalVisible(true)}
        onSwipeDown={() => setModalVisible(false)}
      >
        <Modal
          animationType="slide"
          visible={modalVisible}
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
                    onPress={() => setIsActive([1, 0, 0])}
                    style={[
                      styles.periodButton,
                      isActive[0] == 1 ? styles.activePeriodButton : null,
                    ]}
                  >
                    <Text
                      style={[
                        styles.periodButtonText,
                        isActive[0] == 1 ? styles.activePeroidButtonText : null,
                      ]}
                    >
                      Каждый день
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    onPress={() => setIsActive([0, 1, 0])}
                    style={[
                      styles.periodButton,
                      isActive[1] == 1 ? styles.activePeriodButton : null,
                    ]}
                  >
                    <Text
                      style={[
                        styles.periodButtonText,
                        isActive[1] == 1 ? styles.activePeroidButtonText : null,
                      ]}
                    >
                      Каждый месяц
                    </Text>
                  </TouchableOpacity>
                </View>

                <View style={styles.periodRow}>
                  <TouchableOpacity
                    onPress={() => setIsActive([0, 0, 1])}
                    style={[
                      styles.periodButton,
                      isActive[2] == 1 ? styles.activePeriodButton : null,
                    ]}
                  >
                    <Text
                      style={[
                        styles.periodButtonText,
                        isActive[2] == 1 ? styles.activePeroidButtonText : null,
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
                      setSelectTypeSum([1, 0, 0, 0, 0, 0, 0]);
                      setSum(sum - 10);
                      sum == 10 ? setSum(10) : null;
                    }}
                  >
                    <SvgXml xml={minusIcon} />
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[
                      styles.componentMoney,
                      styles.sumView,
                      selectTypeSum[0] == 1 ? styles.activeSumView : null,
                    ]}
                    onPress={() => setSelectTypeSum([1, 0, 0, 0, 0, 0, 0])}
                  >
                    <Text style={styles.sumViewText}>
                      {sum} ₽
                      {isActive[0] == 1
                        ? " в день"
                        : isActive[1] == 1
                        ? " в месяц"
                        : null}
                    </Text>
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={[styles.componentMoney, styles.plusSum]}
                    onPress={() => {
                      setSum(sum + 10);
                      setSelectTypeSum([1, 0, 0, 0, 0, 0, 0]);
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
                      selectTypeSum[1] == 1 ? styles.activeAutoSumButton : null,
                    ]}
                    onPress={() => {
                      setSelectTypeSum([0, 1, 0, 0, 0, 0]);
                      setSum(200);
                    }}
                  >
                    <Text
                      style={[
                        styles.autoSumButtonText,
                        selectTypeSum[1] == 1
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
                      selectTypeSum[2] == 1 ? styles.activeAutoSumButton : null,
                    ]}
                    onPress={() => {
                      setSelectTypeSum([0, 0, 1, 0, 0, 0]);
                      setSum(400);
                    }}
                  >
                    <Text
                      style={[
                        styles.autoSumButtonText,
                        selectTypeSum[2] == 1
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
                      selectTypeSum[3] == 1 ? styles.activeAutoSumButton : null,
                    ]}
                    onPress={() => {
                      setSelectTypeSum([0, 0, 0, 1, 0, 0]);
                      setSum(900);
                    }}
                  >
                    <Text
                      style={[
                        styles.autoSumButtonText,
                        selectTypeSum[3] == 1
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
                      selectTypeSum[4] == 1 ? styles.activeAutoSumButton : null,
                    ]}
                    onPress={() => {
                      setSelectTypeSum([0, 0, 0, 0, 1, 0]);
                      setSum(1000);
                    }}
                  >
                    <Text
                      style={[
                        styles.autoSumButtonText,
                        selectTypeSum[4] == 1
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
                    selectTypeSum[5] == 1 ? styles.activeInputSelect : null,
                  ]}
                >
                  <View style={styles.componentMoney}>
                    <TextInput
                      onPress={() => {
                        setSelectTypeSum([0, 0, 0, 0, 0, 1]);
                      }}
                      placeholder="Ваша сумма"
                      placeholderTextColor="rgba(183, 183, 183, 1)"
                      keyboardType="number-pad"
                      style={styles.inputSum}
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
                      <Text style={styles.payInfoAtrribute}>Сумма платежа</Text>
                      <Text style={styles.payInfoValue}>{sum} ₽</Text>
                    </View>
                    <View style={styles.divideLine} />
                    <View style={styles.payInfoRow}>
                      <Text style={styles.payInfoAtrribute}>Вид платежа</Text>
                      <Text style={styles.payInfoValue}>
                        {isActive[0] == 1
                          ? "Каждый день"
                          : isActive[1] == 1
                          ? "Каждый месяц"
                          : "Разовый платеж"}
                      </Text>
                    </View>
                  </View>
                </View>
              </View>
            </View>
          </ScrollView>
        </Modal>
      </GestureRecognizer>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 3,
      height: 3,
    },
    shadowOpacity: 0.7,
    shadowRadius: 2,
  },
  mainImage: {
    objectFit: "cover",
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  mainInfo: {
    padding: 20,
    marginTop: 15,
  },
  nameText: {
    fontSize: 16,
    fontFamily: "IBMMedium",
    color: "rgba(52, 52, 52, 1)",
  },
  progressBar: {
    width: "100%",
    height: 5,
    marginTop: 15,
    backgroundColor: "rgba(70, 47, 181, 0.3)",
    borderRadius: 3,
    position: "relative",
  },
  progressFillBar: {
    backgroundColor: "rgba(22, 3, 111, 1)",
    position: "absolute",
    left: 0,
    top: 0,
    height: 5,
    borderRadius: 3,
  },
  progressSum: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
  },
  moneyText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
  },
  buttonsView: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 15,
    gap: 5,
  },
  button: {
    width: "50%",
    alignItems: "center",
    justifyContent: "center",
    height: 35,
    borderRadius: 10,
  },
  detailsButton: {
    borderWidth: 1,
    borderColor: "rgba(22, 3, 111, 1)",
  },
  detailsText: {
    fontFamily: "IBMMedium",
    color: "rgba(22, 3, 111, 1)",
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
});

export default FundCard;
